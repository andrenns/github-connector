from entities.shared.models import db


class Action(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    hash = db.Column(db.String(45), unique=True, nullable=False)
    branch = db.String(db.String(255), nullable=False)
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'), nullable=False)
