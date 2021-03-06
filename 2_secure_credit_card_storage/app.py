import braintree

from flask import Flask, request, render_template
app = Flask(__name__)

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                  merchant_id="use_your_merchant_id",
                                  public_key="use_your_public_key",
                                  private_key="use_your_private_key")

@app.route("/")
def form():
    return render_template("braintree.html")

@app.route("/create_transaction", methods=["POST"])
def create_transaction():
    result = braintree.Transaction.sale({
        "amount": "1000.00",
        "credit_card": {
            "number": request.form["number"],
            "cvv": request.form["cvv"],
            "expiration_month": request.form["month"],
            "expiration_year": request.form["year"]
        },
        "options": {
            "submit_for_settlement": True
        }
    })
    if result.is_success:
        return "<h1>Transaction Successful</h1>ID: {0}".format(result.transaction.id)
    else:
        return "<h1>Transaction Failed</h1>{0}".format(result.message)

@app.route('/create_customer', methods=["POST"])
def create_customer():
    result = braintree.Customer.create({
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "credit_card": {
            "billing_address": {
                "postal_code": request.form["postal_code"]
            },
            "number": request.form["number"],
            "expiration_month": request.form["month"],
            "expiration_year": request.form["year"],
            "cvv": request.form["cvv"]
        }
    })
    if result.is_success:
        return "<h1>Customer created with name: {0}</h1>".format(result.customer.first_name + " " + result.customer.last_name)
    else:
        return "<h1>Error: {0}</h1>".format(result.message)

if __name__ == '__main__':
    app.run(debug=True)
