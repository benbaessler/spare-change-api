from flask import Flask, request, jsonify
import stripe
import json

keys = json.load(open('keys.json', 'r'))
stripe.api_key = keys['api_key']

app = Flask(__name__)

@app.route('/api/auth', methods=['POST'])
def auth():
  card_number = request.args.get('card_number')
  exp_month = request.args.get('exp_month')
  exp_year = request.args.get('exp_year')
  cvc = request.args.get('cvc')

  # Creating customer
  customer = stripe.Customer.create(
    # Add information
  )

  # Creating setup intent
  intent = stripe.SetupIntent.create(customer = customer['id'])

  # Creating payment method
  payment = stripe.PaymentMethod.create(
    type = 'card',
    card = {
      'number': card_number,
      'exp_month': exp_month,
      'exp_year': exp_year,
      'cvc': cvc
    }
  )

  # Confirming setup intent
  try:
    stripe.SetupIntent.confirm(
      intent['id'],
      payment_method = payment
    )
  except stripe.error.CardError as e:
    return jsonify({'status': 'card_error'})


  obj = {
    "id": customer['id'],
    "payment_method": payment['id']
  }

  with open('customer.json', 'w') as f:
    json.dump(obj, f)

  return jsonify({'status': 'success'})


app.run(port=2000)