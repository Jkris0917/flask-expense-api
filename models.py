import json
from datetime import datetime


class Expense:
    def __init__(self, category, amount, date=None, expense_id=None, note=None):
        self.id = expense_id
        self.category = category
        self.amount = float(amount)
        self.note = note
        self.date = date or datetime.now().strftime("%Y-%m-%d. %H:%M:%S")
        
    def to_dict(self):
        return ({
            "id": self.id,
            "category": self.category,
            "amount": self.amount,
            "date": self.date,
            "note": self.note,
        })
        
    def __repr__(self):
        return f"Expense(id={self.id}, category={self.category}, amount={self.amount})"
    
class ExpenseManager:
    def __init__(self,filename="data.json"):
        self.filename = filename
        self.expenses =[]
        self.load()
        
    def _next_id(self):
        return max((e.id for e in self.expenses), default=0) + 1
    
    def add(self,category,amount,note=None):
        expense = Expense(category,amount,note, expense_id=self._next_id())
        self.expenses.append(expense)
        self.save()
        return expense
    
    def get_all(self):
        return self.expenses
    
    def get_by_id(self,expense_id):
        for e in self.expenses:
            if e.id == expense_id:
                return e
        return None
    
    def update(self,expense_id,category=None,amount=None,note=None):
        expense = self.get_by_id(expense_id)
        if expense is None:
            return None
        
        if category is not None:
            expense.category = category
        if amount is not None:
            expense.amount = float(amount)
        if note is not None:
            expense.note = note
            
        self.save()
        return expense
        
    
    def delete(self,expense_id):
        original = len(self.expenses)
        self.expenses = [e for e in self.expenses if e.id != expense_id]
        if len(self.expenses) < original:
            self.save()
            return True
        return False
    
    def total(self):
        return sum(e.amount for e in self.expenses)
    
    def by_category(self):
        result ={}
        for e in self.expenses:
            result[e.category] = result.get(e.category, 0) + e.amount
        return result
    
    def save(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([e.to_dict() for e in self.expenses], f, ensure_ascii=False, indent=2)
            
    def load(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.expenses = [
                    Expense(
                        category=d["category"],
                        amount=d["amount"],
                        note=d.get("note"), 
                        expense_id=d["id"], 
                        date=d['date']
                    ) for d in data
                ]
        except FileNotFoundError:
            self.expenses = []