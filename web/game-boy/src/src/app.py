import os
from flask import Flask, render_template, request, redirect, jsonify, make_response, url_for, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import uuid
import secrets

import traceback

import redis
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, JWTManager, create_access_token, get_jwt_identity, get_jwt

import datetime

import config as cfg

from base import *
from Mailer import Mailer

from sqlalchemy.exc import SQLAlchemyError

import htmlentities

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(256)
app.config['JWT_SECRET_KEY'] = cfg.JWT_SECRET_KEY
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = cfg.JWT_ACCESS_TOKEN_EXPIRES
app.config['JWT_ALGORITHM'] = cfg.JWT_ALGORITHM
app.config['JWT_ERROR_MESSAGE_KEY'] = cfg.JWT_ERROR_MESSAGE_KEY
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = cfg.JWT_REFRESH_TOKEN_EXPIRES
app.config['JWT_HEADER_NAME'] = cfg.JWT_HEADER_NAME
app.config['JWT_HEADER_TYPE'] = cfg.JWT_HEADER_TYPE
app.config['JWT_BLOCKLIST_ENABLED'] = True
app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)

jwt_redis_blocklist = redis.StrictRedis(
    host="redis", port=6379, db=0, decode_responses=True
)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.public_id


@app.route('/register', methods=['POST'])
def signup_user(): 
    try:
        data = request.get_json()
        with session_db() as session:
            user = session.query(User).filter_by(username=data['username']).first()
            if user:
                return jsonify({'error': 'User already exists'})
            hashed_password = generate_password_hash(cfg.PEPPER+data['password']+cfg.SALT, method='scrypt')
            new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, mail=data['mail'], is_verified=True, inscription_date=datetime.datetime.utcnow())
            Mailer().send_verification_mail(new_user.username, new_user.is_verified)
            session.add(new_user) 
            session.commit()
        return jsonify({'message': 'Registered successfully'})
    except: 
        return jsonify({'error': 'Data is invalid'}), 500    


@app.route('/login', methods=['POST']) 
def login_user():
    try:
        data = request.get_json()
        with session_db() as session:
            user = session.query(User).filter_by(username=data['username'], is_verified=True).first()
            if user:
                if check_password_hash(user.password, cfg.PEPPER+data['password']+cfg.SALT):
                    user.last_login_date = datetime.datetime.utcnow()
                    session.commit()
                    if user.is_admin:
                        access_token = create_access_token(identity=user, additional_claims={"username": user.username})
                        return jsonify(access_token=access_token)
                    else:
                        access_token = create_access_token(identity=user, additional_claims={"username": user.username})
                        refresh_token = create_refresh_token(identity=user, additional_claims={"username": user.username})
                        return jsonify({'access_token' : access_token, 'refresh_token': refresh_token})
        return jsonify({'error': 'Login is invalid'}), 401
    except:
        return jsonify({'error': 'Data is invalid'}), 500
    
@app.route("/logout", methods=['GET'])
@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    jwt_redis_blocklist.set(jti, "", ex=cfg.JWT_REFRESH_TOKEN_EXPIRES)
    return jsonify(message=f"{ttype.capitalize()} token successfully revoked")
        
@app.route('/refresh', methods=['GET'])
@jwt_required(refresh=True)
def refresh():
    public_id = get_jwt_identity()
    with session_db() as session:
        current_user = session.query(User).filter_by(public_id=public_id, is_verified=True).one_or_none()
        if current_user:
            ret = {
                'access_token': create_access_token(identity=current_user, additional_claims={"username": current_user.username}),
                'refresh_token': create_refresh_token(identity=current_user, additional_claims={"username": current_user.username})
            }
            jwt_redis_blocklist.set(get_jwt()['jti'], "", ex=cfg.JWT_REFRESH_TOKEN_EXPIRES)
            return jsonify(ret), 200
    return jsonify({'error': 'Invalid refresh token'})


@app.route('/user/<string:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        public_id = get_jwt_identity()
        with session_db() as session:
            current_user = session.query(User).filter_by(public_id=public_id).one_or_none()
            if (current_user.public_id == id and current_user.is_verified) or current_user.is_admin:
                user = session.query(User).filter_by(public_id=id).one_or_none()
                if user:
                    return jsonify(user.as_dict(include_private=True))
                else:
                    return jsonify({'error': 'User does not exist'})
        return jsonify({'error': 'Access unauthorized'}), 401
    except:
        return jsonify({'error': 'Access unauthorized'}), 401
    
@app.route('/users', methods=['GET'])
@jwt_required()
def users():
    try:
        public_id = get_jwt_identity()
        with session_db() as session:
            current_user = session.query(User).filter_by(public_id=public_id).one_or_none()
            users = session.query(User).all()
            return jsonify([user.as_dict() for user in users])
            return jsonify({'error': 'Access unauthorized'}), 401
    except:
        return jsonify({'error': 'Access unauthorized'}), 401

@app.route('/post/<string:id>', methods=['GET', 'POST'])
@jwt_required()
def post(id):
    try:
        if request.method == "POST" and id == "write":
            data = request.get_json()
            public_id = get_jwt_identity()
            if public_id:
                with session_db() as session:
                    current_user = session.query(User).filter_by(public_id=public_id, is_verified=True).one_or_none()
                    if current_user:
                        new_post = Post(post_id=str(uuid.uuid4()), user_id=current_user.id, title=htmlentities.encode(data['title']), content=htmlentities.encode(data['content']), creation_date=datetime.datetime.utcnow())
                        if 'is_private' in data.keys():
                            new_post.is_private = bool(data['is_private'])
                        session.add(new_post)
                        session.commit()
                        return jsonify({'message': 'Post was successfully created'})
                    return jsonify({'error': 'Access unauthorized'}), 401
            return jsonify({'error': 'Access unauthorized'}), 401
        else:
            public_id = get_jwt_identity()
            if public_id:
                with session_db() as session:
                    current_user = session.query(User).filter_by(public_id=public_id, is_verified=True).one_or_none()
                    if current_user:
                        with session_db() as session:
                            post = session.query(Post).filter_by(post_id=id).one_or_none()
                            if not post:
                                return jsonify({'error': f"Post with id {id} does not exist"})
                            if post.user != current_user and post.is_private:
                                return jsonify({'error': 'Access unauthorized'}), 401
                            return jsonify(post.as_dict())
            else:
                return jsonify({'error': 'Access unauthorized'}), 401
    except:
        return jsonify({'error': 'Data is invalid'}), 500

@app.route('/feed', methods=['GET'])
@jwt_required()
def feed():
    try:
        public_id = get_jwt_identity()
        with session_db() as session:
            current_user = session.query(User).filter_by(public_id=public_id, is_verified=True).one_or_none()
            if current_user:
                posts = session.query(Post).filter_by(is_private=False).all()
                return jsonify([post.as_dict() for post in posts])
            return jsonify({'error': 'Access unauthorized'}), 401
    except:
        return jsonify({'error': 'Data is invalid'}), 500

if __name__ == '__main__':
    app.run(cfg.HOST, port=cfg.PORT, debug=cfg.DEBUG)