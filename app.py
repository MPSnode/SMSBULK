from flask import Flask, render_template, request, jsonify
import requests
from twilio.rest import Client

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api_info', methods=['POST'])
def api_info():
    provider = request.form['provider']
    api_key = request.form['api_key']
    api_secret = request.form['api_secret']
    phone_number = request.form['phone_number']
    
    if provider == 'twilio':
        client = Client(api_key, api_secret)
        balance = client.api.balance.fetch().balance
        return jsonify(balance=balance, phone_number=phone_number)
    # Add other providers here
    return jsonify(balance='N/A', phone_number='N/A')

@app.route('/send_sms', methods=['POST'])
def send_sms():
    provider = request.form['provider']
    api_key = request.form['api_key']
    api_secret = request.form['api_secret']
    phone_number = request.form['phone_number']
    targets = request.form['targets'].split(',')
    message = request.form['message']

    results = []
    if provider == 'twilio':
        client = Client(api_key, api_secret)
        for target in targets:
            try:
                msg = client.messages.create(
                    body=message,
                    from_=phone_number,
                    to=target.strip()
                )
                results.append({'target': target.strip(), 'status': 'success', 'log': msg.sid})
            except Exception as e:
                results.append({'target': target.strip(), 'status': 'failed', 'log': str(e)})

    return jsonify(results=results)

if __name__ == '__main__':
    app.run(debug=True)
