from app import db
from sqlalchemy.dialects.postgresql import JSON, JSONB


class Players(db.Model):
    __tablename__ = 'players'

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

class Accounts(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    account = db.Column(JSON)
    accountb = db.Column(JSONB)

    def __init__(self, account):
        self.account = account
        self.accountb = account

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Objects(db.Model):
    __tablename__ = 'objects'

    id = db.Column(db.Integer, primary_key=True)
    object_type = db.Column(db.String)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    def __init__(self, object_type, x, y):
        self.type = object_type
        self.x = x
        self.y = y

    def __repr__(self):
        return '<id {}>'.format(self.id)

class King(db.Model):
    __tablename__ = 'king'
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    king_flag = db.Column(db.Boolean)
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)

    def __init__(self, player_id, king_flag, x, y):
        self.player_id = player_id
        self.king_flag = king_flag
        self.x = x
        self.y = y

    def __repr__(self):
        return '<id {}>'.format(self.id)
