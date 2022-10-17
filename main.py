from tinkoff.invest import Client
import time
import yaml

TOKEN = None

# https://www.openfigi.com/search#!?simpleSearchString=TATNP&page=1&filters=EXCH_CODE:..RX
figis = {
    'BANE': 'BBG004S68758',
    'BANEP': 'BBG004S686N0',
    'TATN': 'BBG004RVFFC0',
    'TATNP': 'BBG004S68829',
    'SBER': 'BBG004730N88',
    'SBERP': 'BBG0047315Y7',
    'NKNC': 'BBG000GQSRR5',
    'NKNCP': 'BBG000GQSVC2',
    'KAZT': 'BBG002B9MYC1',
    'KAZTP': 'BBG002B9T6Y1',
    'PMSB': 'BBG000MZL0Y6',
    'PMSBP': 'BBG000MZL2S9',
    'RTKM': 'BBG004S682Z6',
    'RTKMP': 'BBG004S685M3',
    'KRSB': 'BBG000VPC602',
    'KRSBP': 'BBG000VPC6Y5'
}

def load_from_server(figis: list, max_tries: int = 10):
    for i in range(max_tries):
        try:
            with Client(TOKEN) as client:
                return client.market_data.get_last_prices(figi=figis)
        except Exception:
            time.sleep(1)
            continue

def get_prices(figis: dict[str, str]):
    resp = load_from_server(list(figis.values()))
    prices = dict()
    assert len(figis.keys()) == len(resp.last_prices)
    for ticker, price in zip(figis.keys(), resp.last_prices):
        price_str = str(price.price.units) + "." + str(price.price.nano)
        prices.update({ticker: float(price_str)})
    return prices

def compare_prices(price0: float, price1: float):
    return price0 <= price1

def print_stocks(ticker0: str, ticker1: str, price0: float, price1: float):
    diff = abs(price0 - price1) / min(price0, price1) * 100
    if compare_prices(price0, price1):
        print(f"\x1b[6;30;42m{ticker0}={price0} {ticker1}={price1} diff={diff:,.2f}%\x1b[0m")
    else:
        print(f"{ticker0}={price0} {ticker1}={price1} diff={diff:,.2f}%")

def print_prices(prices: dict[str, float], ticker0: str, ticker1: str):
    price0 = prices[ticker0]
    price1 = prices[ticker1]
    print_stocks(ticker0, ticker1, price0, price1)

with open('config.yaml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
        TOKEN = config['token']
    except yaml.YAMLError as e:
        print(e)

prices = get_prices(figis)
print_prices(prices, 'BANE', 'BANEP')
print_prices(prices, 'TATN', 'TATNP')
print_prices(prices, 'SBER', 'SBERP')
print_prices(prices, 'NKNC', 'NKNCP')
print_prices(prices, 'KAZT', 'KAZTP')
print_prices(prices, 'PMSB', 'PMSBP')
print_prices(prices, 'RTKM', 'RTKMP')
print_prices(prices, 'KRSB', 'KRSBP')
