import stripe
import json

keys = json.load(open('keys.json', 'r'))
stripe.api_key = keys['api_key']

print('Creating customer...')
customer = stripe.Customer.create(
  # Add information
)
print('Success')

print('Creating setup intent...')
intent = stripe.SetupIntent.create(customer = customer['id'])
print('Success')

print('Creating payment method...')
payment = stripe.PaymentMethod.create(
  type = 'card',
  card = {
    'number': '4000002500003155',
    'exp_month': 2,
    'exp_year': 2025,
    'cvc': '123'
  }
)
print('Success')

print('Confirming setup intent...')
stripe.SetupIntent.confirm(
  intent['id'],
  payment_method = payment
)
print('Success')

obj = {
  "id": customer['id'],
  "payment_method": payment['id']
}

with open('customer.json', 'w') as f:
  json.dump(obj, f)

print('Data written to customer.json')
