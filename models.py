from app import db
from sqlalchemy.dialects.postgresql import JSON


class Result(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    player = db.Column(JSON)

    def __init__(self, player):
        self.player = player

    def __repr__(self):
        return '<id {}>'.format(self.id)
