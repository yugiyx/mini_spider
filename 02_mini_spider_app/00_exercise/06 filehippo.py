import os
import time
import requests
from pyquery import PyQuery as pq

base_url = 'https://filehippo.com'
key_words = 'foobar2000'


def get_page(url):
    headers = {}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            return r
        return None
    except requests.RequestException as e:
        print('Error:', e.args)
        return None


def parse_total_page_num(html):
    doc = pq(html.text)
    total_page = doc('.pager-container a:nth-last-child(2)').text()
    return total_page


def parse_urls(html):
    doc = pq(html.text)
    urls = doc('#program-history-list a')
    for url in urls.items():
        yield base_url + url.attr('href')


def parse_one_page(html):
    doc = pq(html.text)
    url = doc('.program-header-download-link').attr('href')
    doc = pq(get_page(url).text)
    file_name = doc('.breadcrumbs div:nth-last-child(2)').text() + '.exe'
    url = base_url + doc('#download-link').attr('href')
    return url, file_name


def download_file(url, file_name):
    if not os.path.exists(key_words):
        os.makedirs(key_words)
    path = key_words + '/' + file_name
    if not os.path.exists(path):
        print(path, '正在下载')
        r = requests.get(url)
        with open(path, 'wb') as f:
            f.write(r.content)
    else:
        print(file_name, '已存在，无需下载')


def main():
    history_url = base_url + '/download_' + key_words + '/history/'
    html = get_page(history_url)
    total_page = parse_total_page_num(html)
    print('总页数:', total_page, '页')
    for page in range(1, int(total_page) + 1):
        print('查询第' + str(page) + '页', time.strftime('%Y-%m-%d %H:%M:%S'))
        next_url = history_url + str(page) + '/'
        print(next_url)
        html = get_page(next_url)
        url_list = parse_urls(html)
        for url in url_list:
            html = get_page(url)
            url, file_name = parse_one_page(html)
            download_file(url, file_name)


if __name__ == '__main__':
    main()
    print('==========下载结束==========', time.strftime('%Y-%m-%d %H:%M:%S'))
