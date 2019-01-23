import csv
import json
# from pymongo import MongoClient


class DataOutput(object):

    def __init__(self, data_name):
        self.datas = []
        self.data_name = data_name

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def save_2_text(self, content):
        '''
        存储为纯文本
        :parameter:
        content str格式文本
        :return:
        打印Succesfully save data
        '''
        with open(self.data_name, 'a', encoding='utf-8') as f:
            f.write(content + '\n')
        return 'Succesfully save data'

    def save_2_csv(self, content):
        '''
        存储为CSV格式纯文本
        :return:
        '''
        with open(self.data_name, 'a', encoding='utf-8') as f:
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
        with open(self.data_name, 'a', encoding='utf-8') as f:
            f.write(json.dumps(content, indent=2, ensure_ascii=False) + '\n')
        return 'Succesfully save data'

    def save_2_binary(self):
        '''
        存储为二进制格式，图片、文件等
        :return:
        '''
        pass

    # def save_2_mongodb(self, content):
    #     '''
    #     存储为JSON格式纯文本
    #     :parameter:
    #     content dict格式数据
    #     :return:
    #     打印Succesfully save data
    #     '''
    #     client = MongoClient()
    #     db = client[self.data_name]
    #     collection = db[self.data_name]
    #     collection.insert(self, content)
    #     return 'Succesfully save data'


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
    # 测试save_2_mongodb()
    test5 = DataOutput('test')
    # mongo_data1 = {
    #     'id': 10001,
    #     'text': '我爱你中国',
    #     'reposts_count': 50,
    #     'comments_count': 0,
    #     'attitudes_count': 100,
    # }
    # mongo_data2 = {
    #     'id': 10002,
    #     'text': '我爱你武汉',
    #     'reposts_count': 49,
    #     'comments_count': 0,
    #     'attitudes_count': 99,
    # }
    # test5.save_2_mongodb(mongo_data1)
    # test5.save_2_mongodb(mongo_data2)
