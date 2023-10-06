import time

import requests


# https://coinglass.readme.io/reference/instrument
# https://coinglass.readme.io/reference/open-interest not relevant due the same price for all exchanges !!! blyat'


# SUKA Perpetual Market!!!
# https://coinglass.readme.io/reference/perpetual-market

def get_data(url):
    url = url  # lol
    headers = {
        "accept": "application/json",
        "coinglassSecret": "98a0b94cfc9543f2abfdc14cd51649b8"
    }
    response = requests.get(url, headers=headers)
    return response.json()['data']


def extract_coins_name(database_from_instrument):
    global coin_list
    for coin_data in database_from_instrument:
        coin_name = coin_data['baseAsset']
        if coin_name not in coin_list:
            coin_list.append(coin_name)
        else:
            continue
    #    print(f'found coins: {len(coin_list)}')
    return coin_list


def coin_prices_database(data, coin):
    # print(data)
    data_temp = data[coin]
    for exchange_pos in range(len(data_temp)):
        exchange_name = data_temp[exchange_pos]["exchangeName"]
        # print(exchange_name)
        price = data_temp[exchange_pos]["price"]
        coin_prices[coin][exchange_name] = price
        # print("coin_prices_database debug: ", exchange_name, price)  # debug line
    return coin_prices


def api_request_count_timer(timer):
    request_count = timer
 #   if request_count == 29:  # free API has restrictions  for 30 requests per minute. 1 were used per first data request (get data from instrument).
    print("Free 30 API requests ended. Needs to wait one minute. Please be patient.")
    # time.sleep(61)
    for second in range(62):
        if second == 0:
            print(0, "%", sep="", end="")
        elif second == 30:
            print(50, "%", sep="", end="")
        elif second == 61:
            print(100, "%")
        else:
            print("|", sep="", end="")
        time.sleep(1)


def prices_table(coin_prices):
    print(coin_prices)
    print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format('Coin', 'Binance', 'OKX',
                                                                                         'Bybit',
                                                                                         'BingX', 'Bitget', 'dYdX',
                                                                                         'Kraken', 'Huobi', 'CoinEx'))
    for coin_name, value in coin_prices.items():
        # print("!!!", coin_name)
        print("{:<10}".format(coin_name), end=" ")
        exchanges = ['Binance', 'OKX', 'Bybit', 'BingX', 'Bitget', 'dYdX', 'Kraken', 'Huobi', 'CoinEx']
        for exchange in exchanges:
            if exchange not in value:
                print("{:<10}".format("N/a"), end=" ")
            else:
                print("{:<10}".format(value[exchange]), end=' ')
            if exchange == 'CoinEx':
                print('')


def exchange_diff(coin_prices):
    for coin in coin_prices:  # btc, eth, link, etc.
        #
        min_price = min(coin_prices[coin].values())
        max_price = max(coin_prices[coin].values())
        difference = 100 - min_price / (max_price / 100)

        if difference > 2:
            print('\n', coin)
            for exchange, price in coin_prices[coin].items():
                if price == min_price:
                    print(f'MIN price: {exchange} > {min_price}')
                elif price == max_price:
                    print(f'MAX price: {exchange} > {max_price}')
            print(f"Difference between exchanges: {difference}%")
        else:
            continue


coin_list = []
# looks like 'instrument' module is lightweight so lets use it for coin name database.
instrument_url = "https://open-api.coinglass.com/public/v2/instrument"
# print(get_data(instrument_url))  # debugging line

data = get_data(instrument_url)
for exchange in data:
    extract_coins_name(data[exchange])
print(coin_list)  # now we have all coins from all exchanges.

coin_prices = {}
request_count = 0
to_check = len(coin_list)  # left xxx coins
for coin in coin_list[::]:  # change coin value here (positions from-till)
    # print(coin)
    perpetual_market_url = f"https://open-api.coinglass.com/public/v2/perpetual_market?symbol={coin}"
    try:
        data = get_data(perpetual_market_url)
    except:
        continue
    request_count += 1
    to_check -= 1
    print(to_check)
    print(request_count)
    if request_count == 29:
        api_request_count_timer(request_count)  # enables timer for 61 seconds
        request_count = 0
    coin_prices[coin] = {}
    coin_prices = coin_prices_database(data, coin)  # creates dict with {coin1:{exch1:price, exch2:...}, ...}
    print(coin_prices)
    # min_fund_rate = min(coin.values())
    # max_fund_rate = max(coin.values())
    # profit = round((max_fund_rate - min_fund_rate), 4)

prices_table(coin_prices)
exchange_diff(coin_prices)
