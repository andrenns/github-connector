from entities.shared.models import db


class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(45), unique=True, nullable=False)
    url = db.String(db.String(255), nullable=False)
    actions = db.relationship('Action', backref='repo', lazy=True)
