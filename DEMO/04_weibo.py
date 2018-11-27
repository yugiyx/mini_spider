import requests
from pyquery import PyQuery as pq
from pymongo import MongoClient

url = 'https://m.weibo.cn/api/container/getIndex'


def get_one_page(page):

    params = {
        'type': 'uid',
        'value': '3268555654',
        'containerid': '1076033268555654',
        'page': page,
    }
    try:
        response = requests.get(url, params=params)
        print(response.url)
        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        print('Error:', e.args)


def parse_one_page(json_data):

    items = json_data['data']['cards']
    for item in items:
        item = item['mblog']
        yield {
            'id': int(item['id']),
            'text': pq(item['text']).text().replace(' ', ''),
            'reposts_count': item['reposts_count'],
            'comments_count': item['comments_count'],
            'attitudes_count': item['attitudes_count'],
        }


def save_to_mongodb(data):

    client = MongoClient()
    db = client['weibo']
    collection = db['weibo']
    collection.insert(data)


def main():

    for page in range(1, 70):
        data = get_one_page(page)
        results = parse_one_page(data)
        for result in results:
            print(result)
            save_to_mongodb(result)


if __name__ == '__main__':
    main()
