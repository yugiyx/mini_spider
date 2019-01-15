import json
import re
import time
import requests


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
    pattern = re.compile(
        r'<dd>.*?board-index-.*?>(.*?)</i>.*?<img data-src="(.*?)"' +
        r'.*?title="(.*?)"\sdata.*?star">(.*?)</p>.*?releasetime">(.*?)</p>' +
        r'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>', re.S)
    items = re.findall(pattern, html)
    print('There are', len(items), 'results.')
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip() if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip(),
        }


def write_to_file(content):
    with open('results.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, indent=2, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    # print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(0.5)
