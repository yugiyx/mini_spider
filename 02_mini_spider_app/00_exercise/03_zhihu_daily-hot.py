import json
import requests
from pyquery import PyQuery as pq


def get_one_page(url):

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
            'AppleWebKit/537.36 (KHTML, like Gecko) ' +
            'Chrome/67.0.3396.99 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.exceptions.RequestException:
        return None


def parse_one_page(html):
    doc = pq(html)
    items = doc('.explore-feed.feed-item')
    for item in items.items():
        yield {
            'question': item.find('h2').text(),
            'author': item.find('.author-link-line').text(),
            'answer': pq(item.find('.content').html()).text(),
        }


def write_to_file(content):
    with open('results.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.write('\n' + '=' * 50 + '\n')


def main():
    url = 'https://www.zhihu.com/explore'
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    main()
