import stripe
import math
import json

keys = {}
with open('keys.json', 'r') as file:
  keys = json.loads(file.read())

stripe.api_key = keys['api_key']

def calculate_change(amount):
  if str(amount)[-2:] == '00':
    return 100
  amount_float = amount / 100
  rounded_up = math.ceil(amount_float) * 100
  return rounded_up - amount

def charge_change(amount, customer_id):
  stripe.Charge.create(
    amount = calculate_change(amount),
    currency = 'eur',
    customer = customer_id,
    description = 'sct'
  )

# instance = stripe.Customer.create(
#   email = 'test@gmail.com',
#   name = 'Marle',
#   phone = 'Gobermann',
# )

# payment = stripe.Customer.create_source(instance.id, source = 'tok_amex')