import requests
from bs4 import BeautifulSoup
import sys


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    sys.setrecursionlimit(4000)
    headers = {
        'content-type': 'text/html; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    url ="http://220.134.173.17/gameking/card/ocg_list.asp?call_item=7&call_data=%B4%B6%A5d&call_sql=Select%20*%20from%20ocg%20where%20ocg_type%20=%20%27%B4%B6%A5d%27%20order%20by%20ocg_no%20asc&Page=1"

    response = requests.get(url=url, headers=headers, timeout=15)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find_all('table')

    cards = table[1].find_all('tr')

    print(type(cards))

