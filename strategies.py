import re
import requests
import pandas as pd
import plotly as pt


pair = input('Pair: ').upper()
pip = 0.0001
api_key = 'K1hPKDKmhp3vFddRWLhL'
date_format = 'yyyy-mm-dd'
start_date, end_date = input(f'Start Date {date_format}: '), input(f'End Date {date_format}: ')

url = requests.get(f'https://marketdata.tradermade.com/api/v1/pandasDF?currency={pair}&api_key={api_key}'
                   f'&start_date={start_date}&end_date={end_date}&format=records&fields=close')
url_json = url.json()
Closing_Prices = pd.json_normalize(url_json)



def double_zero():
    # This function looks for the double 00 pattern in all closing price_data
    # On the daily chart for the date range specified
    price_data = Closing_Prices[pair]
    jpy_pairs = re.compile(r'JPY')
    regex_object = jpy_pairs.findall(pair)
    if regex_object != ['JPY']:
        regex_pattern = re.compile(r'\d{1,3}\.\d\d\d[0][0]')
        non_jpy = ['{:.5f}'.format(i) for i in price_data if len(str(i)) > 3]
        print(non_jpy)
        pattern = re.findall(regex_pattern, str(non_jpy))
        if len(pattern) == 0:
            return 'No Double Zero Closes'
        else:
            return f' the closes for this time period are {pattern}'

    if regex_object == ['JPY']:
        regex_pattern = re.compile(r'\d{1,3}\.\d[0][0]')
        jpy_list = ['{:.3f}'.format(i) for i in price_data if len(str(i)) < 4]
        pattern = re.findall(regex_pattern, str(jpy_list))
        if len(pattern) == 0:
            return 'No Double Zero Closes' 
        else:
            print(len(pattern))
            return f' the closes for this time period are {pattern}'