import stripe
import math
import json

keys = json.load(open('keys.json', 'r'))
stripe.api_key = keys['api_key']

def calculate_change(amount):
  if str(amount)[-2:] == '00':
    return 50
  amount_float = amount / 100
  rounded_up = math.ceil(amount_float) * 100
  return rounded_up - amount

def create_charge(amount, customer_id):
  stripe.Charge.create(
    amount = amount,
    currency = 'eur',
    customer = customer_id,
    description = 'sct'
  )

def charge(amount, customer_id):
  _keys = json.load(open('keys.json', 'r'))
  change = calculate_change(amount)
  if change >= 50:
    create_charge(change, customer_id)
  else:
    _keys['saved_change'] += change
    with open('keys.json', 'w') as f:
      json.dump(_keys, f)

    f = open('keys.json', 'r')
    keys_updated = json.load(f)

    change = keys_updated['saved_change']

    if change >= 50:
      create_charge(change, customer_id)
      keys_updated['saved_change'] = 0
      with open('keys.json', 'w') as f:
        json.dump(keys_updated, f)