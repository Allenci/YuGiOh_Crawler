import shutil
import requests
from bs4 import BeautifulSoup
import sys
import os


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    sys.setrecursionlimit(4000)
    headers = {
        'content-type': 'text/html; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    domain = "http://220.134.173.17/gameking/card/"
    url = domain + "ocg_list.asp?call_item=7&call_data=%B4%B6%A5d&call_sql=Select%20*%20from%20ocg%20where%20ocg_type%20=%20%27%B4%B6%A5d%27%20order%20by%20ocg_no%20asc&Page=1"

    home = BeautifulSoup(requests.get(url=url, headers=headers, timeout=15).content, 'html.parser')
    cards = home.find_all('table')[1].find_all('tr')
    cards = cards[1:-1]  # 移除table頭尾標題

    card_number = cards[0].find_all('td')[1].contents[0].strip()  # 卡號
    card_name = cards[0].find_all('td')[2].contents[0].strip()  # 卡名
    link = domain + cards[0].find_all('a')[0].get('href')  # 內容連結
    dir_name = "D:/ggggg/yugioh_download_images"  # 圖檔資料夾

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    image_url = BeautifulSoup(requests.get(url=link, headers=headers, timeout=15).content, 'html.parser').find('img')['src']
    r = requests.get(image_url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True
        filename = dir_name + '/' + card_number + '_' + card_name + '.jpg'
        print(card_number, card_name)
        with open(filename, 'wb') as tmp_file:
            shutil.copyfileobj(r.raw, tmp_file)
            tmp_file.close()

        print("Image sucessfully Downloaded: ", card_name)

    else:
        print("Image can not be retreived")
