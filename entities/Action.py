from entities.shared.models import db


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(45), unique=True, nullable=False)
    url = db.String(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    repo_id = db.Column(db.Integer, db.ForeignKey('repo_id'), nullable=False)
    messages = db.relationship('Message', backref='action', lazy=True)
    commits = db.relationship('Commit', backref='action', lazy=True)
