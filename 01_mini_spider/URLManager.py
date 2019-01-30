class UrlManager(object):
    def __init__(self):
        self.new_urls = []  # 未爬取URL列表
        self.old_urls = []  # 已爬取URL列表

    def has_new_url(self):
        '''
        判断是否有未爬取的URL
        :return:
        '''
        return self.new_url_size() != 0

    def get_new_url(self):
        '''
        获取一个未爬取的URL
        :return:
        '''
        # 弹出正数第一个URL
        new_url = self.new_urls.pop(0)
        self.old_urls.append(new_url)
        return new_url

    def get_new_urls(self):
        '''
        获取全部未爬取的URL
        :return:
        '''
        # 弹出全部URL
        new_urls = self.new_urls[:]
        self.old_urls = self.new_urls[:]
        self.new_urls = []
        return new_urls

    def add_new_url(self, url):
        '''
         将新的URL添加到未爬取的URL集合中
        :parameter:
        url 单个URL
        :return:
        '''
        if url is None:
            return None
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.append(url)

    def add_new_urls(self, urls):
        '''
        将新的URLS添加到未爬取的URL集合中
        :parameter:
        urls URL列表，生成器
        :return:
        '''
        if urls is None:
            return None
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        '''
        获取未爬取URL集合的s大小
        :return:
        '''
        return len(self.new_urls)

    def old_url_size(self):
        '''
        获取已经爬取URL集合的大小
        :return:
        '''
        return len(self.old_urls)

    def remove_duplication(self, flag):
        '''
        去重判断
        :parameter:
        :flag 去重标志
        :return:
        未重复，返回去重标志。重复，返回None
        '''
        with open('download_log.txt', 'a+', encoding='utf-8') as f:
            f.seek(0)
            if flag in f.read():
                return None
            else:
                return flag

    def add_duplication(self, flag):
        '''
        记录去重标志
        :parameter:
        :flag 去重标志
        :return:
        未重复，返回去重标志。重复，返回None
        '''
        with open('download_log.txt', 'a', encoding='utf-8') as f:
            f.write(flag + '\n')
