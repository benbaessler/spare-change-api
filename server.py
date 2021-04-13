from flask import Flask, jsonify, request
import stripe
import charge
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
  payload = request.data

  keys = json.load(open('keys.json', 'r'))

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
    amount = obj.amount
    if obj.description == 'sct':
      # print(event)
      print('Change charged!', amount)
      
    else:
      print('Status:', obj.status)
      print('Amount:', amount)
      # print(event)
      customer = json.load(open('customer.json', 'r'))
      change.charge(amount, keys['customer_id'])
  else:
    print('Not relevant')

  return jsonify({'status': 'success'})

if __name__ == '__main__':
  app.run(port=4242)