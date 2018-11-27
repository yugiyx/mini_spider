import json
import re
import os
import time
import requests
from pyquery import PyQuery as pq

url = 'https://www.toutiao.com/search_content/'


def get_page(page, keyword):
    params = {
        'offset': page,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'gallery',
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException as e:
        print('Error:', e.args)
        return None


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
        'AppleWebKit/537.36 (KHTML, like Gecko) ' +
        'Chrome/67.0.3396.99 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # print(response.url)
            return response.text
        return None
    except requests.RequestException as e:
        print('Error:', e.args)
        return None


def parse_page(json_data):
    items = json_data['data']
    for item in items:
        yield item['article_url']


def parse_one_page(html):
    doc = pq(html)
    title = doc('title').text()
    pattern = re.compile(r'gallery.*?parse\("(.*?)"\),', re.S)
    result = re.search(pattern, html)
    if result:
        data = json.loads(result.group(1).replace('\\', ''))
        if data and 'sub_images' in data.keys():
            sub_images = data['sub_images']
            images = [item['url'] for item in sub_images]
            return {
                'title': title,
                'images': images,
            }


def save_to_folder(folder_name):
    path = time.strftime('%Y%m%d') + '/' + folder_name
    os.makedirs(path.strip())
    return path


def write_to_files(folder_name, contents):
    path = './' + save_to_folder(folder_name) + '/'
    i = 1
    for item in contents:
        file_path = path + str(i) + '.jpg'
        print('正在下载', file_path)
        r = requests.get(item)
        with open(file_path, 'wb') as f:
            f.write(r.content)
        i += 1


def main():
    for page in range(1):
        html_list = get_page(page, '街拍')
        for url in parse_page(html_list):
            html = get_one_page(url)
            result = parse_one_page(html)
            write_to_files(result['title'], result['images'])


if __name__ == '__main__':
    main()
