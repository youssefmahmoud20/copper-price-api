from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def home():
    return 'Bloomberg Copper API is running!'


@app.route('/get-copper-price')
def get_copper_price():
    try:
        url = 'https://www.bloomberg.com/quote/LMCADS03:COM?embedded-checkout=true'
        headers = {'User-Agent': 'Mozilla/5.0'}

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        price_element = soup.find(
            'div',
            class_='sized-price media-ui-SizedPrice_extraLarge-05pKbJRbUH8- media-ui-SizedPrice_tabular-THpKTXeBUGw-'
        )

        if price_element:
            price = price_element.text.strip()
            return jsonify({'price': price})
        else:
            return jsonify({'error': 'Copper price not found'})

    except Exception as e:
        return jsonify({'error': str(e)})


# 🟢 Required for Render Deployment
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
