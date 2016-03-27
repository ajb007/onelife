from app import db
from sqlalchemy.dialects.postgresql import JSON, JSONB


class Player(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer)
    player = db.Column(JSON)
    playerb = db.Column(JSONB)

    def __init__(self, account_id, player):
        self.account_id = account_id
        self.player = player
        self.playerb = player

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    account = db.Column(JSON)
    accountb = db.Column(JSONB)

    def __init__(self, account):
        self.account = account
        self.accountb = account

    def __repr__(self):
        return '<id {}>'.format(self.id)
