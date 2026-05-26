from flask import Flask,jsonify,request
from models import ExpenseManager
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
manager = ExpenseManager(filename=os.getenv("DATA_FILE","data.json"))

@app.route('/expenses', methods=["GET"])
def get_all():
    return jsonify([e.to_dict() for e in manager.get_all()]), 200

@app.route("/expenses/<int:id>", methods=["GET"])
def get_one(id):
    expense = manager.get_by_id(id)
    if expense is None:
        return jsonify({"message": f"Expense {id} not found"}), 404
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
    
    expense = manager.add(data['category'],amount, data.get("note"))
    return jsonify(expense.to_dict()),201

@app.route("/expenses/<int:id>", methods=["PUT"])
def update_expense(id):
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
    result = manager.update(
        id,
        category=data.get('category'),
        amount=data.get('amount'), 
        note=data.get('note')
        )
    if result is None:
        return jsonify({"error":f"Expense {id} not found"}), 404
    return jsonify(result.to_dict()), 200

@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expense(id):
    deleted = manager.delete(id)
    if not deleted:
        return jsonify({"error": f"Expense {id} not found"}), 404
    return jsonify({"message": "Deleted successfully", "id":id}) ,200

@app.route("/summary",methods=['GET'])
def summary():
    return jsonify({
        "total_expenses": len(manager.get_all()),
        "total_amount": manager.total(),
        "by_category": manager.by_category()
    }),200
    
if __name__ == "__main__":
    app.run(debug=True)
