from flask import Flask, request, jsonify
import requests
import concurrent.futures

app = Flask(__name__)

def fetch_data(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            return response.json().get("numbers", [])
    except requests.Timeout:
        pass
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
    
    return []

@app.route('/numbers')
def get_numbers():
    urls = request.args.getlist('url')
    
    # Using ThreadPoolExecutor to fetch data from multiple URLs concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_data, urls))

    # Merge and sort the integers from all the fetched URLs
    merged_numbers = sorted(set(number for numbers in results for number in numbers))

    return jsonify({"numbers": merged_numbers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
