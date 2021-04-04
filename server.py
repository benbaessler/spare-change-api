import stripe
import transfer
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
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
    obj = event.data.object
    if obj.description == 'sct':
      print('Change charged!', obj.amount)
      
    else:
      print('Status:', obj.status)
      print('Amount:', obj.amount)
      transfer.charge_change(obj.amount, keys['customer_id'])
  else:
    print('Not relevant')

  return jsonify({'status': 'success'})

if __name__ == '__main__':
  app.run(port=4242)