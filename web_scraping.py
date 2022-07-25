from bs4 import BeautifulSoup
import requests
import re
import csv

import pandas as pd

rows = {'Blockchains': []}
url = "https://www.defipulse.com/"


def links_scraper(url):
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")
    all_groupings = soup.find_all("a")
    rows_list = [i.get('href') for i in all_groupings]
    return rows_list


def table_scraper(url):
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, "html.parser")
    top_50_projects = [i.get_text() for i in soup.find_all(re.compile("td"))]
    pat = ' '.join(top_50_projects)
    return pat


cat = table_scraper(url)
li = list(cat.split('%'))
hat = [[i] for i in li]
data_frame = pd.DataFrame(hat)
print(data_frame)
# data_frame.to_csv('Top 50 Projects.csv', index=False)
