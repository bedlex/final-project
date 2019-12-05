from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from app_base import app,db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
# User Auth Flow Mixin
from flask_login import UserMixin

# Import login_manager
from app_base import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# One-to-many Relationship
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(150), unique = True ,nullable = False)
    photourl = db.Column(db.String(500))
    password = db.Column(db.String(300), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.now)
    articles = db.relationship('Article', backref='owner', lazy="dynamic")

    def __init__(self, username, firstname, lastname, email , password):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = self.set_password(password)

    def __repr__(self):
        return "{} has been created".format(self.username)

    def set_password(self,password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(100), nullable = False)
    title = db.Column(db.String(400),unique = True, nullable = False)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    article = db.Column(db.Text, nullable = False)
    location = db.Column(db.String(400), nullable = False)
    source = db.Column(db.String(150))
    date_created = db.Column(db.DateTime, default = datetime.now)
    photopath = db.Column(db.Text)
    def __init__(self,title, category, author, article, location ,source):
        self.category = category
        self.title = title
        self.author = author
        self.article = article
        self.location = location
        self.source = source
    def __repr__(self):
        return "The Title is {} and the user is {}".format(self.title, self.author)
