import re
import os
import time
import requests
from pyquery import PyQuery as pq

url = 'http://image.fengniao.com/'
total_page = 10
bbs_url = 'http://bbs.fengniao.com/forum/10557303.html'


def get_page(url):
    headers = {
        'Cookie': '12345',
    }
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r
        return None
    except requests.RequestException as e:
        print('Error:', e.args)
        return None


def parse_first_page(html):
    doc = pq(html.text)
    items = doc('.main .listBox').find('.pic.pic75')
    for lis in items.items():
        yield lis.attr('href')


def parse_next_page(html):
    doc = html.json().get('data')
    for item in doc:
        if 'url' in item.keys():
            yield item.get('url')


def parse_one_page(html):
    doc = pq(html.text)
    title = doc('title').text().replace('_组图-蜂鸟网', '').replace('|', '').strip()
    html = doc('html').html().replace('\\', '')
    pattern = re.compile(r'pic_url":"(.*?)","pic_url_s', re.S)
    results = re.findall(pattern, html)
    return {
        'title': title,
        'images': results,
    }


def parse_bbs_page(html):
    doc = pq(html.text)
    title = doc('title').text().replace('【有图】', '').strip()
    html = doc('.postMain.module1200').html()
    pattern = re.compile(r'class="img".*?src="(.*?)"/></a>', re.S)
    results = re.findall(pattern, html)
    return {
        'title': title,
        'images': results,
    }


def create_one_folder(folder_name, folder_name2):
    path_is_exists = False
    path = folder_name.strip()
    for root, dirs, files in os.walk('.'):
        if path in dirs:
            path_is_exists = True
    if not path_is_exists:
        path = folder_name2 + '/' + time.strftime('%Y%m%d') + '/' + path
        os.makedirs(path)
        return path
    else:
        return None


def download_pictures(url_list):
    for url in url_list:
        if 'slide' in url:
            html = get_page(url)
            results = parse_one_page(html)
            write_to_files(results['title'], results['images'], 'dashi')


def write_to_files(folder_name, contents, folder_name2):
    path = create_one_folder(folder_name, folder_name2)
    if path:
        print(folder_name, '开始下载')
        i = 1
        for item in contents:
            file_path = path + '/' + str(i) + '.jpg'
            r = requests.get(item)
            with open(file_path, 'wb') as f:
                f.write(r.content)
            i += 1
    else:
        print(folder_name, '已存在，无需下载')


def main_dashi(url=url, total_page=total_page):
    print('查询第 1 页', time.strftime('%Y-%m-%d %H:%M:%S'))
    html = get_page(url)
    url_list = parse_first_page(html)
    download_pictures(url_list)
    for page in range(2, total_page + 1):
        next_url = url + \
            'index.php?action=getList&class_id=192&sub_classid=0&page=' + \
            str(page) + '&not_in_id='
        print('查询第', str(page), '页', time.strftime('%Y-%m-%d %H:%M:%S'))
        html = get_page(next_url)
        url_list = parse_next_page(html)
        download_pictures(url_list)


def main_bbs(url=bbs_url):
    url_list = []
    html = get_page(url)
    doc = pq(html.text)
    total_page = re.sub("\D", "", doc(
        '.page.module1200 span').text())
    if not total_page:
        total_page = 1
    for page in range(1, int(total_page) + 1):
        next_url = url[:-5] + '_' + str(page) + url[-5:]
        html = get_page(next_url)
        results = parse_bbs_page(html)
        url_list = url_list + results['images']
    write_to_files(results['title'], url_list, 'bbs')


if __name__ == '__main__':
    main_bbs()
    print('==========下载结束==========', time.strftime('%Y-%m-%d %H:%M:%S'))
