import json
import re

import pyinputplus as pyip
ACCOUNT_VALUE = 500.00

position_size = int(input('Position Size: '))
# current_price = c.get_rate(currency_pair[:3], currency_pair[3:]).__round__(5 if currency_pair.split('D')[1] != 'JPY'
# else 3)
currency_pair = pyip.inputStr(prompt='Pair ', allowRegexes=r' ')
with open('../Data Files/Margin.Json', 'r') as f:
    base_margin = json.load(f)


class Margin_req:
    """I want to be able to create a trade object that tells me the base margin req for a trade (1000 units)
    and then store that object in a JSON file that I can then pull from whenever I am doing analysis for a trade"""
    def __init__(self, pair, margin_req):
        self.pair = pair
        self.margin_req = margin_req

    def write_to_file(self, filename):
        with open(filename, 'r') as file:
            config = json.load(file)

        config["Pairs"].append({self.pair: self.margin_req})
        with open(filename, 'w') as file:
            json.dump(config, file, indent=4)

