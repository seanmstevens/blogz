from app import db
from hashutils import make_pw_hash
from datetime import datetime

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70))
    body = db.Column(db.String(500))
    pubdate = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner, pubdate=None):
        self.title = title
        self.body = body
        self.owner = owner
        if pubdate is None:
            pubdate = datetime.now()
        self.pubdate = pubdate

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(18), unique=True)
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)
