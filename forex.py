import csv

import pyinputplus as pyip
from forex_python.converter import CurrencyRates
import json
import datetime as dt
import pandas as pd

# Input
LOSS_LIMIT = 0.02
ACCOUNT_VALUE = pyip.inputInt('Account Value: ')
c = CurrencyRates()
currency_pair = input('Pair: ').upper()
lot_size = pyip.inputInt('Lot Size: ')
current_price = c.get_rate(currency_pair[:3], currency_pair[3:]).__round__(3 if currency_pair[3:] == 'JPY'
                                                                           else 5)
play_type = input('Buy|Sell: ')
with open('../Data Files/Margin.Json', 'r') as f:
    base_margin = json.load(f)


def max_position_size(trade_size=lot_size):
    # I need to put in guardrails to let me know if I need to add a pair to the margin file and so not crash the script
    # each time it fails. Could use Try:Except block IndexError: list index out of range
    try:
        base_pair_cost = [i[currency_pair] for i in base_margin['Pairs'] if currency_pair in i]
        margin_req = [base_pair_cost[0] * trade_size / 1000]
        if margin_req[0] <= ACCOUNT_VALUE * 0.33:
            return margin_req[0], trade_size
        while margin_req[0] > ACCOUNT_VALUE * 0.33:
            trade_size -= 1000
            margin_req = [base_pair_cost[0] * trade_size / 1000]
        return margin_req[0], trade_size
    except ValueError:
        return "Pair not in Margin file"


def pip_value(trade_size=max_position_size()[0]):
    if currency_pair[:3] == 'JPY':
        pip = 0.01 / current_price * trade_size
        conversion = c.convert(currency_pair[:3], 'USD', pip)
        return conversion.__round__(3)
    else:
        pip = 0.0001 / current_price * lot_size
        conversion = c.convert(currency_pair[:3], 'USD', pip)
        return conversion.__round__(3)


def maximum_pip_loss():
    pip = pip_value()
    return round((ACCOUNT_VALUE * LOSS_LIMIT) / pip)


def move_point(shift=int(-4 if currency_pair[:3] != 'JPY' else -2), number=maximum_pip_loss(), base=10):
    return round(number * base ** shift, 5)


def market_entry_stop_loss(direction=play_type.title()):
    if direction == 'Buy':
        pip_shift = move_point().__round__(5)
        stop_loss = current_price - pip_shift
        return round(stop_loss, 5 if currency_pair[:3] != 'JPY' else 3)

    elif direction == 'Sell':
        pip_shift = move_point()
        stop_loss = current_price + pip_shift
        return round(stop_loss, 5 if currency_pair[:3] != 'JPY' else 3)


def delayed_entry_stop_loss(direction=play_type.title()):
    entry_price = pyip.inputFloat('What is the entry price')
    if direction == 'Buy':
        pip_shift = move_point()
        stop_loss = entry_price - pip_shift
        return round(stop_loss, 5 if currency_pair[:3] != 'JPY' else 3)

    elif direction == 'Sell':
        pip_shift = move_point()
        stop_loss = entry_price + pip_shift
        return round(stop_loss, 5 if currency_pair[:3] != 'JPY' else 3)


a = max_position_size()
b = maximum_pip_loss()
c = pip_value()
d = market_entry_stop_loss()

trade_journal = pd.DataFrame(
    {
        'Pair': currency_pair,
        'Size': a[1],
        'Pip': c,
        'Cost': a[0],
        'Stop Loss': d,
        'Date': dt.date.today()
    },
    index=range(1)
)

with open('../Data Files/Trade Journal.csv', 'a') as f:
    writer = csv.writer(f)
    writing = trade_journal.to_csv(f, header=False)

print(trade_journal)
