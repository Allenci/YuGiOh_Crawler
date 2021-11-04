import shutil
import requests
from bs4 import BeautifulSoup
import sys
import os
import time


def print_hi(name):
    print(f'Hi, {name}')


def get_headers():
    return {
        'content-type': 'text/html; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }


def set_recursion_limit():
    sys.setrecursionlimit(4000)


def get_domain():
    return "http://220.134.173.17/gameking/card/"


def get_url_query():
    return "ocg_list.asp?call_item=7&call_data=%B4%B6%A5d&call_sql=Select%20*%20from%20ocg%20where%20ocg_type%20=%20%27%B4%B6%A5d%27%20order%20by%20ocg_no%20asc&Page="


def get_soup_instance(url, headers, timeout=15):
    return BeautifulSoup(requests.get(url=url, headers=headers, timeout=15).content, 'html.parser')


def set_download_dir(name):
    if not os.path.exists(name):
        os.mkdir(name)


def get_download_dir_name():
    return "D:/yugioh_download_images"


def trim(card):
    return card.strip()


def remove_backslash(card):
    return card.replace('\\', "-")


def remove_slash(card):
    return card.replace('/', "-")


def download():

    page_from = 1
    page_to = 993

    domain = get_domain()
    query = get_url_query()

    dir_name = get_download_dir_name()
    set_recursion_limit()
    set_download_dir(dir_name)

    while page_from <= page_to:
        time.sleep(2)
        print('正在第' + str(page_from) + '頁...')
        url_source = domain + query + str(page_from)
        home = get_soup_instance(url_source, get_headers())
        cards = home.find_all('table')[1].find_all('tr')
        cards = cards[1:-1]  # 移除table頭尾標題

        i = 1
        while i <= len(cards):
            link = domain + cards[i-1].find_all('a')[0].get('href')
            image = get_soup_instance(link, get_headers()).find('img')
            card_number = remove_slash(remove_backslash(trim(cards[i-1].find_all('td')[1].contents[0])))
            card_name = remove_slash(remove_backslash(trim(cards[i-1].find_all('td')[2].contents[0])))

            if image is not None:
                r = requests.get(image['src'], stream=True)
                if r.status_code == 200:
                    r.raw.decode_content = True
                    filename = dir_name + '/' + card_number + '_' + card_name + '.jpg'
                    with open(filename, 'wb') as tmp_file:
                        shutil.copyfileobj(r.raw, tmp_file)
                        tmp_file.close()
                else:
                    print("X 圖片" + card_name + "_" + card_number + "不存在")

            i += 1  # increment card

        page_from += 1  # increment page


if __name__ == '__main__':
    # 下載圖片
    download()

    print("---- Download finished!! ----")
