from entities.shared.models import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    message = db.Column(db.BLOB, unique=True, nullable=False)
    action_id = db.Column(db.Integer, db.ForeignKey('action.id'), nullable=False)
