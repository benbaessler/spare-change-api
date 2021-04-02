import stripe
import json
import math
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
  # Simple deserialization:
  # json_payload = json.loads(request.data)
  # event = stripe.Event.construct_from(json_payload, stripe.api_key)
  # print(event.type)
  # print(type(event.data.object))
  # print(event.data.object.id)

  # With signature verification:
  payload = request.data

  keys = {}

  with open('keys.json', 'r') as file:
    keys = json.loads(file.read())

  endpoint_secret = keys['endpoint_secret']

  sig_header = request.headers.get('stripe-signature')

  try:
    event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
  except ValueError as e:
    # Invalid payload
    return jsonify({'error': str(e)})
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return jsonify({'error': str(e)})

  if event.type == 'charge.succeeded':
    charge_amount = event.data.object.amount
    print('Change:', str(round_up(charge_amount)))
  else:
    print('Not relevant')

  return jsonify({'status': 'success'})

def round_up(amount):
  
  if str(amount)[-2:] == '00':
    return 1

  amount_int = amount / 100
  rounded_up = math.ceil(amount_int)
  return round(rounded_up - amount_int, 2)

if __name__ == '__main__':
  app.run(port=4242)