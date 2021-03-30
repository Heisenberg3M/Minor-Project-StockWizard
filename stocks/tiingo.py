import requests

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 52cf4ba23a37819947b982159a5c027b4678f7dc'
}

def get_meta_data(ticker):
    url = "https://api.tiingo.com/tiingo/daily/{}".format(ticker)
    response = requests.get(url, headers=headers)
    return response.json()

def get_price_data(ticker):
    url = "https://api.tiingo.com/tiingo/daily/{}/prices".format(ticker)
    response = requests.get(url, headers=headers)
    return response.json()[0]

