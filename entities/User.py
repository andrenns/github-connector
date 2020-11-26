from entities.shared.models import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(45), unique=True, nullable=False)
    actions = db.relationship('Action', backref='user', lazy=True)

