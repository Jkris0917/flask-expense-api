from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Expense(db.Model):
    __tablename__ = "expenses"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "amount": self.amount,
            "note": self.note,
            "created_at": self.created_at.strftime("%Y-%m-%d %H-%M-%S") if self.created_at else None
        }
        
    def __repr__(self):
        return f"Expense(id='{self.id}', category='{self.category}', amount='{self.amount}')"
    
    