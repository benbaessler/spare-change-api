import stripe
import math
import json

file = open('keys.json', 'r')
keys = json.load(file)

stripe.api_key = keys['api_key']

def calculate_change(amount):
  if str(amount)[-2:] == '00':
    return 100
  amount_float = amount / 100
  rounded_up = math.ceil(amount_float) * 100
  return rounded_up - amount

def charge_change(amount, customer_id):
  change = calculate_change(amount)
  if change >= 50:
    stripe.Charge.create(
      amount = change,
      currency = 'eur',
      customer = customer_id,
      description = 'sct'
    )
  else:
    keys['saved_change'] += change
    with open('keys.json', 'w') as file:
      json.dump(keys, file)

# instance = stripe.Customer.create(
#   email = 'test@gmail.com',
#   name = 'Marle',
#   phone = 'Gobermann',
# )

# payment = stripe.Customer.create_source(instance.id, source = 'tok_amex')