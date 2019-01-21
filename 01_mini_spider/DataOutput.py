import json


class DataOutput(object):

    def __init__(self):
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def save_2_text(self):
        '''
        存储为纯文本
        :return:
        '''
        pass

    def save_2_csv(self):
        '''
        存储为CSV格式纯文本
        :return:
        '''
        pass

    def save_2_json(self):
        '''
        存储为JSON格式纯文本
        :return:
        '''
        pass

    def save_2_binary(self):
        '''
        存储为二进制格式，图片、文件等
        :return:
        '''
        pass
