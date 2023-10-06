coin_prices = {
    'BTC': {'Binance': 25881.7, 'Bybit': 25880, 'OKX': 25893.5, 'Bitget': 25873, 'Deribit': 25896.5, 'BingX': 25884.8,
            'Bitfinex': 25908, 'dYdX': 25888, 'Huobi': 25886.9, 'Kraken': 25893.0, 'CoinEx': 25903.86},
    'ETH': {'Binance': 1635.243714, 'Bybit': 1634.5, 'OKX': 1635.37, 'Deribit': 1635.15, 'Bitget': 1635.09,
            'dYdX': 1634.9, 'BingX': 1634.9, 'Bitfinex': 1636.1, 'Huobi': 1635.05, 'Kraken': 1636.5, 'CoinEx': 1632.66},
    'LINK': {'Binance': 6.185, 'Bybit': 6.184, 'OKX': 6.195, 'BingX': 6.184, 'Bitget': 6.184, 'dYdX': 6.187,
             'Huobi': 6.1829, 'CoinEx': 6.187, 'Kraken': 6.186},
    'BNB': {'Binance': 215.14, 'Bybit': 214.85, 'OKX': 215.04, 'Bitget': 215.03, 'BingX': 215.05, 'Huobi': 214.903,
            'CoinEx': 215.03},
    'TRX': {'Binance': 0.07897, 'OKX': 0.07907, 'Bybit': 0.079, 'Bitget': 0.07902, 'dYdX': 0.0791, 'BingX': 0.07903,
            'Huobi': 0.078983, 'CoinEx': 0.079078, 'Kraken': 0.079106}}


def exchange_diff(coin_prices):
    for coin in coin_prices:  # btc, eth, link, etc.
        print(coin)
        min_price = min(coin_prices[coin].values())
        max_price = max(coin_prices[coin].values())

        for exchange, price in coin_prices[coin].items():
            if price == min_price:
                print(f'MIN price: {exchange} > {min_price}')
            elif price == max_price:
                print(f'MAX price: {exchange} > {max_price}')
        difference = 100 - min_price / (max_price / 100)
        print(difference)



# profit = round((max_fund_rate - min_fund_rate), 4)


exchange_diff(coin_prices)
