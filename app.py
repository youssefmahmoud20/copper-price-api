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

        price_element = soup.find('div', class_='sized-price media-ui-SizedPrice_extraLarge-05pKbJRbUH8- media-ui-SizedPrice_tabular-THpKTXeBUGw-')
        
        if price_element:
            price = price_element.text.strip()
            return jsonify({'price': price})
        else:
            return jsonify({'error': 'Copper price not found'})
    except Exception as e:
        return jsonify({'error': str(e)})

# 🔴 NEW ROUTE: this will poke your WordPress cron URLs
@app.route('/trigger-wp-cron')
def trigger_wp_cron():
    urls = [
        'https://powerelectricsupply.com/?force_update_lme=1',
        'https://powerelectricsupply.com/wp-cron.php?doing_wp_cron=1',
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    }

    results = []
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            results.append({'url': url, 'status': r.status_code})
        except Exception as e:
            results.append({'url': url, 'error': str(e)})

    return jsonify({'status': 'ok', 'results': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
