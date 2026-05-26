from flask import Flask,jsonify,request
from models import db,Expense
from dotenv import load_dotenv
from sqlalchemy import func
import os

load_dotenv()
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/expenses', methods=["GET"])
def get_all():
    expenses = Expense.query.all()
    return jsonify([e.to_dict() for e in expenses]), 200

@app.route("/expenses/<int:id>", methods=["GET"])
def get_one(id):
    expense = Expense.query.get(id)
    if expense is None:
        return jsonify({"error": f"Expense {id} not found"}), 404
    return jsonify(expense.to_dict()),200

@app.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No JSON body provided"}),400
    
    if not "category" in data or not 'amount' in data:
        return jsonify({"error": "'category' and 'amount' are required"}), 400
    
    try:
        amount = float(data["amount"])
        if amount <= 0:
            return jsonify({"error": "Amount must be positive"}), 400
    except ValueError:
        return jsonify({"error": "Amount must be a number"}), 400
    
    expense = Expense(
        category=data['category'],
        amount=amount, 
        note=data.get("note")
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify(expense.to_dict()),201

@app.route("/expenses/<int:id>", methods=["PUT"])
def update_expense(id):
    expense = Expense.query.get(id)
    if expense is None:
        return jsonify({"error": f"Expense {id} not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"message": "No JSON body provided"}), 400
    
    if "amount" in data:
        try:
           data["amount"] = float(data["amount"])
           if data["amount"] <= 0:
                return jsonify({"error": "Amount must be positive"}), 400
        except ValueError:
            return jsonify({"error": "Amount must be a number"}), 400
        
    if "category" in data:
        expense.category = data["category"]
        
    if "note" in data:
        expense.note = data["note"]
    
    db.session.commit()
    return jsonify(expense.to_dict()), 200

@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    expense = Expense.query.delete(id)
    if expense is None:
        return jsonify({"error": f"Expense {id} not found"}), 404
    
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Deleted successfully", "id":id}) ,200

@app.route("/summary", methods=['GET'])
def summary():
    results = db.session.query(
        Expense.category,
        func.sum(Expense.amount)
    ).group_by(Expense.category).all()

    by_category = {row[0]: row[1] for row in results}

    total_expenses = Expense.query.count()       
    total_amount = sum(by_category.values())      

    return jsonify({
        "total_expenses": total_expenses,
        "total_amount": total_amount,
        "by_category": by_category
    }), 200
    
if __name__ == "__main__":
    app.run(debug=True)
