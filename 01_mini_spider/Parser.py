import re
from pyquery import PyQuery as pq


class HtmlParser(object):

    def parse_urls(self, response):
        '''
        获取需要下载的URL和标题
        :parameter:
        response 下载器得到的Response对象
        :return:
        需要下载的URL和标题
        '''
        if response is None:
            return None
        doc = pq(response.text)
        if doc('title'):
            # 获取大师版首页的URL列表
            items = doc('.main .listBox').find('.pic.pic75')
            for item in items.items():
                title = item.attr('title').replace('|', '').strip()
                url = item.attr('href')
                # 通过判断url是否含有slide，去掉非画廊内容
                if 'slide' in url:
                    print('解析到==>', title)
                    yield url
        else:
            # 获取后续页URL列表
            doc = response.json().get('data')
            for item in doc:
                title = item.get('title').replace('|', '').strip()
                url = item.get('url')
                if 'slide' in url:
                    print('解析到==>', title)
                    yield url

    def parse_data(self, response):
        '''
        第二级解析函数，获取有效数据
        :parameter：
        response 下载器得到的Response对象
        :return:
        标题和需下载图片URL列表
        '''
        if response is None:
            return None
        doc = pq(response.text)
        if 'slide' in response.url:
            title = doc('title').text().replace(
                '_组图-蜂鸟网', '').replace('|', '').strip()
            html = doc('html').html().replace('\\', '')
            urls = re.findall(
                r'pic_url":"(.*?)","pic_url_s', html, re.S)
        elif 'bbs' in response.url:
            title = doc('title').text().replace('【有图】', '').strip()
            html = doc('.postMain.module1200').html()
            urls = re.findall(
                r'class="img".*?src="(.*?)"/></a>', html, re.S)
        return {
            'title': title,
            'url': urls,
        }
