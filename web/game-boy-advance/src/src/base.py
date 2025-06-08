from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime, Float, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.sql import func
import sqlalchemy_jsonfield
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import config as cfg

main_engine = create_engine(cfg.DATABASE_URI)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    public_id = Column(String(40))
    username = Column(String(255))
    mail = Column(String(64))
    password = Column(String(255))
    inscription_date = Column(DateTime(timezone=True), server_default=func.now())
    last_login_date = Column(DateTime(timezone=True), server_default=func.now())
    is_verified = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    posts = relationship("Post", backref="user", lazy='subquery', foreign_keys="Post.user_id")
    
    def as_dict(self, include_private=False):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        del result['password']
        del result['id']
        if self.posts:
            if include_private:
                result.update({'posts': [post.as_dict() for post in self.posts]})
            else:
                result.update({'posts': [post.as_dict() for post in self.posts if not post.is_private]})
        return result

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    post_id = Column(String(40))
    title = Column(String(255))
    content = Column(Text)
    creation_date = Column(DateTime(timezone=True), server_default=func.now())
    is_private = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    def as_dict(self):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        del result['id']
        del result['user_id']
        return result
            
            
#Base.metadata.drop_all(main_engine)
#Base.metadata.create_all(main_engine)
session_db = sessionmaker(bind=main_engine)