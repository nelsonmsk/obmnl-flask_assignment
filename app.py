# Import libraries

from flask import Flask, redirect, request, render_template, url_for
#import numpy  as np

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
    ]

# Read operation: List all transactions
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation: Display add transaction form
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': float(request.form['amount'])
        }
    
        # Append the new transaction to the list
        transactions.append(transaction)
    
        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))

    # Render the form template to display the add transaction form
    return render_template("form.html")

# Update operation: Display edit transaction form

@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']
        amount = float(request.form['amount'])

        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break

        # Redirect to the transactions list page
        return redirect(url_for("get_transactions"))

    # Find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

# Delete operation: Delete a transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    
    # Redirect to the transactions list page
    return redirect(url_for("get_transactions"))


# Search operation: Search a transaction
@app.route("/search", methods=["GET", "POST"])
def search_transaction():
    if request.method == 'POST':
        # Extract the updated values from the form fields
        min_amount = float(request.form['min_amount'])
        max_amount = float(request.form['max_amount'])
        filtered_transactions = []
        
        # Find the transactions with  it from the list
       # values = np.arrange(min_amount, max_amount)
        for transaction in transactions:
           # if transaction['amount'] in values:
           if float(transaction['amount']) > min_amount and float(transaction['amount']) < max_amount:
                filtered_transactions.append(transaction)
                
        # Render the transactions template to display the search results
        return render_template("transactions.html", transactions=filtered_transactions)
    
    # Render the form template to display the add transaction form
    return render_template("search.html")

# Balance operation: Total balance for all transactions
@app.route("/balance/")
def total_balance():  
    total_amount = 0.00
    # Find all the transactions amounts and add them to the new list
    for transaction in transactions:
        total_amount = total_amount + float(transaction['amount'])

    # Render the transactions template to display the search results
    return render_template("transactions.html", total_bal=total_amount)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)