import requests

# built for the focus group.
# here used only one module that will contact with internet
# to understand how it works (from where im getting an info) you may read below an official 'Coinglass' api docks
# https://coinglass.readme.io/reference/funding-rate
# after getting the info all other operations is performing locally on a pc.

# below official python link for to understand how to install 'requests' module on your computer.
# please note: before that, you will need to install python on your computer.
# https://pypi.org/project/requests/

# now profit value is more than 0.5.
# you may play with that value for getting more accurate output that will be relevant for you.
profit_value_to_show = 0.5

url = "https://open-api.coinglass.com/public/v2/funding"
headers = {
    "accept": "application/json",
    "coinglassSecret": "98a0b94cfc9543f2abfdc14cd51649b8"
}

response = requests.get(url, headers=headers)
main_data = response.json()['data']

fund_dict = {}
# debug code.

for i in range(len(main_data[0]['uMarginList'])):
    print(main_data[0]['uMarginList'][i]['exchangeName'])

for coin_pos in range(len(main_data)):
    for exchange_pos in range(len(main_data[0]['uMarginList'])): # BTC "umarginlist" has length 11.
        exchange_name = main_data[coin_pos]['uMarginList'][exchange_pos]['exchangeName']
        try:
            coin_rate = round(main_data[coin_pos]['uMarginList'][exchange_pos]['rate'], 4)
            # rounded due to 8+ numbers after a comma.
        except:
            continue

        if exchange_name not in ['Bitfinex', 'Gate', 'Bitget', 'CoinEx', 'Kraken', 'BingX', 'TRB', 'dYdX']:
            fund_dict[exchange_name] = coin_rate

    min_fund_rate = min(fund_dict.values())
    max_fund_rate = max(fund_dict.values())
    profit = round((max_fund_rate - min_fund_rate), 4)

    if min_fund_rate < 0:
        profit = round((max_fund_rate + abs(min_fund_rate)), 4)
    else:
        profit = round((max_fund_rate - min_fund_rate), 4)

    if profit >= profit_value_to_show:
        print(main_data[coin_pos]['symbol'])
        for exchange, fund_rate in fund_dict.items():
            if fund_rate == min_fund_rate:
                print(f"Minimal Funding Rate has {exchange}: {fund_rate}")
            elif fund_rate == max_fund_rate:
                print(f"Maximal Funding Rate has {exchange}: {fund_rate}")

        print(f'Profit: {round((max_fund_rate - min_fund_rate), 4)}')


