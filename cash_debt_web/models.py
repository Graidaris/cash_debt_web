from cash_debt_web import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    debtors = db.relationship('Debtor', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)    
    
    def __repr__(self):
        return f'<User {self.id}, email: {self.email}>'
    
    
class Debtor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    money = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    FK_user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    
    def __repr__(self):
        return f'<Debtor {self.id}>'