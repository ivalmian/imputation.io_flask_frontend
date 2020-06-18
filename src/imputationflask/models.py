from imputationflask import db
from datetime import datetime


HASH_STRING_SIZE = 128 
COMMENT_STRING_SIZE = 1000
EMAIL_STRING_SIZE = 254



class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement = True)
    email = db.Column(db.String(EMAIL_STRING_SIZE),nullable=True)
    comment = db.Column(db.String(COMMENT_STRING_SIZE), nullable=False)
    timestamp = db.Column(db.TIMESTAMP(timezone=False), nullable=False, default=datetime.now())
    user_hash_id = db.Column(db.String(HASH_STRING_SIZE), db.ForeignKey('User.hash_id'), nullable=False)

    user = db.relationship('User', backref=db.backref('comment', lazy=True))

    def __repr__(self):
        return f'<Comment {self.id}>' 

class CensusImputationRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.TIMESTAMP(timezone=False), nullable=False, default=datetime.now())
    user_hash_id = db.Column(db.String(HASH_STRING_SIZE), db.ForeignKey('User.hash_id'), nullable=False)
    imputation_hash_id = db.Column(db.String(HASH_STRING_SIZE), db.ForeignKey('CensusImputation.hash_id'), nullable=False)

    user = db.relationship('User', backref=db.backref('comment', lazy=True))
    imputation = db.relationship('CensusImputation', backref=db.backref('censusimputationrequest', lazy=True))

    def __repr__(self):
        return f'<Imputation request {self.id}>' 
    
class User(db.Model):
    hash_id = db.Column(db.String(HASH_STRING_SIZE), primary_key= True)
    fingerprint = db.Column(db.JSON)

    def __repr__(self):
        return f'<User with hash {self.hash_id}>' 

class CensusImputation(db.Model):
    hash_id = db.Column(db.String(HASH_STRING_SIZE),primary_key= True)
    input_object = db.Column(db.JSON)
    output_object = db.Column(db.JSON)

    def __repr__(self):
        return f'<Census imputation with hash {self.hash_id}>' 
