import csv
import json
import os

import time
from pymongo import MongoClient
from Downloader import HtmlDownloader


class DataOutput(object):

    def __init__(self):
        self.downloader = HtmlDownloader()

    def save_2_text(self, content):
        '''
        存储为纯文本
        :parameter:
        content str类型
        :return:
        打印Succesfully save data
        '''
        if content is None:
            return None
        with open(self.data_name, 'a', encoding='utf-8') as f:
            f.write(content + '\n')
        return 'Succesfully save data'

    def save_2_csv(self, content):
        '''
        存储为CSV格式纯文本
        :parameter:
        content list类型
        :return:
        '''
        if content is None:
            return None
        with open(self.data_name, 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(content)
        return 'Succesfully save data'

    def save_2_json(self, content):
        '''
        存储为JSON格式纯文本
        :parameter:
        content dict或dict-list混合体(Python无JSON数据类型，只有这种类JSON混合体)
        :return:
        打印Succesfully save data
        '''
        if content is None:
            return None
        with open(self.data_name, 'a', encoding='utf-8') as f:
            f.write(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
        return 'Succesfully save data'

    def save_2_binary(self, name, content):
        '''
        存储为二进制格式，图片、文件等
        :parameter:
        name 存储的文件夹名字
        :return:
        '''
        if content is None:
            return None
        path = 'data/' + time.strftime('%Y%m%d') + '/' + name
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        with open(file_path, 'wb') as f:
            f.write(r.content)
        return 'Succesfully save data'

    def save_2_mongodb(self, content):
        '''
        存储为JSON格式纯文本
        :parameter:
        content dict类型
        :return:
        打印Succesfully save data
        '''
        if content is None:
            return None
        client = MongoClient('localhost', 27017)
        db = client[self.data_name]
        collection = db[self.data_name]
        collection.insert_one(content)
        return 'Succesfully save data'


if __name__ == '__main__':
    test1 = DataOutput('text.txt')
    # 测试save_2_text()
    text_data = '我爱你中国，我爱你武汉'
    test1.save_2_text(text_data)
    # 测试save_2_text()
    test2 = DataOutput('csv_demo.csv')
    csv_data = ['我爱你中国', '我爱你武汉']
    test2.save_2_csv(csv_data)
    test2.save_2_csv(csv_data)
    # 测试save_2_json()
    test3 = DataOutput('data.txt')
    json_data = [
        {
            'name': '我爱你中国',
            'age': 18,
            'city': 'wuhan',
        },
        {
            'name': '我爱你武汉',
            'age': 17,
            'city': 'wuhan',
        }
    ]
    test3.save_2_json(json_data)
    # 测试save_2_binary 暂无
    # 测试save_2_mongodb()
    test5 = DataOutput('test')
    mongo_data1 = {
        'id': 10001,
        'text': '我爱你中国',
        'reposts_count': 50,
        'comments_count': 0,
        'attitudes_count': 100,
    }
    mongo_data2 = {
        'id': 10002,
        'text': '我爱你武汉',
        'reposts_count': 49,
        'comments_count': 0,
        'attitudes_count': 99,
    }
    test5.save_2_mongodb(mongo_data1)
    test5.save_2_mongodb(mongo_data2)
