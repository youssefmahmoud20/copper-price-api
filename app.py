from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return 'Copper API (Metal.com) is running!'

@app.route('/get-copper-price')
def get_copper_price():
    try:
        url = 'https://www.metal.com/en/future/LME_CA_3M'
        headers = {'User-Agent': 'Mozilla/5.0'}

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        price_elements = soup.find_all('span', class_='FuturePriceDetail_value__MsdBq')

        if len(price_elements) >= 5:
            copper_price = price_elements[4].text.strip()
            return jsonify({'price': copper_price})
        else:
            return jsonify({'error': f'Found only {len(price_elements)} elements. Expected at least 5.'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
