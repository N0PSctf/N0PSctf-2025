import jinja2
from flask import Flask, render_template_string, render_template, request, url_for, redirect, send_file, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import datetime
import secrets
import random
import json

db = SQLAlchemy()

# lemme sanitize a bit, i hate hackerz
# i had a cybersec class where they told about sqli, xss and ssti, so let's filter all of that stuff
def sanitize(field):
    if (("{%" in field)
    or ("%}" in field) 
    or ("{" in field and "}" in field) 
    or ("<" in field)
    or (">" in field) 
    or ("os" in field)
    or ("union" in field.lower())
    or ("select" in field.lower())):
        return "SANITIZED"
    return field

class SlotMachine():
    def __init__(self):
        self.jackpot = 1000.0
        self.chars = ["7", "100", "coin", "rocket", "party"]
        self.odds = [0.2, 0.4, 0.5, 0.6, 0.7]
        self.gains = [0, 100.0, 25.0, 10.0, 5.0]
        self.length = 5
    
    def roll(self, user):
        result = []
        gain = 0.0
        user.money -= 1.0

        if not user.stats:
            user.stats = json.dumps({"played": 0, "avg_gain": 0.0})

        stats = user.stats
        if isinstance(user.stats, str):
            try:
                stats = json.loads(user.stats)
            except json.JSONDecodeError:
                stats = {"played": 0, "avg_gain": 0.0}

        for i in range(self.length):
            char = random.choice(self.chars)
            odds = self.odds[self.chars.index(char)]
            if random.random() < odds:
                result.append(char)
            else:
                result.append("skull")

        for char in list(set(result)):
            if char != "skull" and result.count(char) == 3:
                gain = self.gains[self.chars.index(char)]
            elif char != "skull" and result.count(char) == 4:
                gain = self.gains[self.chars.index(char)] * 1.5
            elif char != "skull" and result.count(char) == 5:
                gain = self.gains[self.chars.index(char)] * 2.0
                if char == "7":
                    gain += self.jackpot
                    self.jackpot = 1000.0
        if gain == 0.0:
            self.jackpot += 1.0

        user.money += gain

        stats["played"] += 1
        stats["avg_gain"] = (stats["avg_gain"] * (stats["played"] - 1) + gain - 1) / stats["played"]
        user.stats = json.dumps(stats) 

        db.session.commit()
        return result, gain


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    money = db.Column(db.Float(), nullable=False)
    stats = db.Column(db.Text(), nullable=False)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:nTf8NV5d3H224gdJ@localhost/main_db"
app.config["SECRET_KEY"] = secrets.token_urlsafe(64)
app.slotMachine = SlotMachine()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

db.init_app(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            if request.form.get("username") == "":
                return "Username cannot be empty"
            if request.form.get("email") == "":
                return "Email cannot be empty"
            if request.form.get("password") == "":
                return "Password cannot be empty"
            user = Users(username=request.form.get("username"),
                        email=request.form.get("email"),
                        password=generate_password_hash(request.form.get("password"), method='scrypt'),
                        money=1000.0,
                        stats='{"played": 0, "avg_gain": 0}')
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
        except:
            return "A user with this username already exists"
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        if user and check_password_hash(user.password, request.form.get("password")):
            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/")
@login_required
def home():
    return render_template("casino.html")

@app.route("/export")
@login_required
def export_data():
    template = open("template.csv", "r").read()
    csv = jinja2.Template(template).render(
        username=sanitize(current_user.username),
        email=sanitize(current_user.email),
        created_at=current_user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        money=current_user.money,
        stats=json.dumps(current_user.stats)
    )
    response = make_response(render_template_string(csv))
    response.headers["Content-Disposition"] = f"attachment; filename={secrets.token_urlsafe(8)}.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

@app.route("/play")
@login_required
def play():
    if current_user.money == 0:
        return jsonify({"error": "You have no money left"})
    else:
        result, gain = app.slotMachine.roll(current_user)
        return jsonify({"result": result, "gain": gain, "jackpot": app.slotMachine.jackpot, "money": current_user.money})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
