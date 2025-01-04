from flask import Flask, request, jsonify

app = Flask(__name__)


budgets = []
transactions = []


def generate_id(collection):
    return len(collection) + 1




@app.route('/budgets', methods=['post'])
def create_budget():
    data = request.get_json()
    if not data or 'name' not in data or 'amount' not in data:
        return jsonify({'error': ' name or amount for the budget not found '}), 400
    
    budget_id = generate_id(budgets)
    new_budget = {
        'id': budget_id,
        'name': data['name'],
        'amount': data['amount'],
        'balance': data['amount']
    }
    
    budgets.append(new_budget)
    return jsonify(new_budget), 201


@app.route('/budgets', methods=['get'])
def get_budgets():
    return jsonify(budgets)


@app.route('/budgets/<int:budget_id>', methods=['put'])
def update_budget(budget_id):
    data = request.get_json()
    budget = next((b for b in budgets if b['id'] == budget_id), None)
    
    if not budget:
        return jsonify({'error': 'Budget not found'}), 404
    
    if 'amount' in data:
        budget['amount'] = data['amount']
    
    if 'balance' in data:
        budget['balance'] = data['balance']
    
    return jsonify(budget)


@app.route('/budgets/<int:budget_id>', methods=['delete'])
def delete_budget(budget_id):
    global budgets
    budgets = [b for b in budgets if b['id'] != budget_id]
    return jsonify({'message': 'Budget is deleted '})




@app.route('/transactions', methods=['POST'])
def create_transaction():
    data = request.get_json()
    if not data or 'budget_id' not in data or 'amount' not in data or 'description' not in data:
        return jsonify({'error': ' budget_id, amount or description not found'}), 400
    
    transaction_id = generate_id(transactions)
    new_transaction = {
        'id': transaction_id,
        'budget_id': data['budget_id'],
        'amount': data['amount'],
        'description': data['description']
    }
    
    transactions.append(new_transaction)
    
    
    budget = next((b for b in budgets if b['id'] == data['budget_id']), None)
    if budget:
        budget['balance'] -= data['amount']
    
    return jsonify(new_transaction), 201


@app.route('/transactions', methods=['GET'])
def get_transactions():
    return jsonify(transactions)


@app.route('/transactions/<int:transaction_id>', methods=['PUT'])
def update_transaction(transaction_id):
    data = request.get_json()
    transaction = next((t for t in transactions if t['id'] == transaction_id), None)
    
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    
    if 'amount' in data:
        
        budget = next((b for b in budgets if b['id'] == transaction['budget_id']), None)
        if budget:
            budget['balance'] += transaction['amount']  
            budget['balance'] -= data['amount'] 
        
        transaction['amount'] = data['amount']
    
    if 'description' in data:
        transaction['description'] = data['description']
    
    return jsonify(transaction)


@app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    global transactions
    transaction = next((t for t in transactions if t['id'] == transaction_id), None)
    
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    
    
    budget = next((b for b in budgets if b['id'] == transaction['budget_id']), None)
    if budget:
        budget['balance'] += transaction['amount']
    
    transactions = [t for t in transactions if t['id'] != transaction_id]
    return jsonify({'message': 'Transaction deleted successfully'})



if __name__ == '__main__':
    app.run(debug=True)

