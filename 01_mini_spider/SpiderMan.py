import time
from URLManager import UrlManager
from Downloader import HtmlDownloader
from Parser import HtmlParser
from DataOutput import DataOutput


class SpiderMan(object):
    def __init__(self):
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl_image(self, start_url, total_page, __page=2):
        '''
        爬取蜂鸟大师板块和技法板块的画集
        :parameter:
        :start_url 参数为需要下载的文章URL
        :total_page 下载页数
        :__page 扩展页数起始参数，用户请勿设定
        :return:无
        '''
        manager = UrlManager()
        # 添加入口URL
        if 'image' in start_url or 'academy' in start_url:
            manager.add_new_url(start_url)
            # 判断url管理器中是否有新的url
            while(manager.has_new_url()):
                try:
                    # 从URL管理器获取新的url
                    new_url = manager.get_new_url()
                    # HTML下载器下载网页
                    html = self.downloader.download(new_url)
                    # 通过关键词判断是否是二级网页
                    if 'slide' in new_url:
                        # HTML解析器抽取二级网页数据
                        data = self.parser.parse_data(html)
                        self.crawl_items(data)
                    else:
                        # HTML解析器抽取一级网页数据
                        data = self.parser.parse_urls(html)
                        manager.add_new_urls(data)
                except Exception as e:
                    print('爬取失败==>', e)
            # 爬取后续页数
            if __page <= total_page:
                if 'image' in start_url:
                    next_url = '%s/index.php?action=getList&class_id=192&sub_classid=0&page=%s&not_in_id=' % (
                        start_url, str(__page))
                elif 'academy' in start_url:
                    next_url = '%s/index.php?action=getList&class_id=190&sub_classid=0&page=%s&not_in_id=' % (
                        start_url, str(__page))
                print('开始爬取==>第', str(__page), '页')
                return self.crawl_image(next_url, total_page, __page + 1)
        else:
            print('网址有错误，请检查')

    def crawl_bbs(self, start_url):
        '''
        爬取蜂鸟论坛帖子里面的图片
        :parameter:
        :start_url 参数为需要下载的文章URL
        :return:无
        '''
        pass

    def crawl_items(self, data):
        '''
        :parameter:
        :data 主程序传过来的数据
        格式如下{'title':xxxx,'url':[xxxx,xxxx,xxxx]}
        :return:无
        '''
        manager = UrlManager()
        # 获取文章标题
        title = data.get('title')
        # 去重
        if manager.remove_duplication(title):
            manager.add_new_urls(data.get('url'))
            # 下载图片文件
            while(manager.has_new_url()):
                print('下载开始==>', title)
                image_urls = manager.get_new_urls()
                # 使用序列修改文件名
                for index, url in enumerate(image_urls):
                    print('下载中==>图片%s' % (index + 1))
                    data = self.downloader.download(url)
                    self.output.save_2_binary(title, index + 1, data)
            # 全部下载完成，增加去重标志
            if not manager.has_new_url():
                manager.add_duplication(title)
                print('下载完成==>')
        else:
            print('重复|无需下载==>', title)

# 蜂鸟大师板地址
image_url = 'http://image.fengniao.com'
# 蜂鸟技法板地址
academy_url = 'http://academy.fengniao.com'
# 蜂鸟论坛帖子地址
bbs_url = 'http://bbs.fengniao.com/forum/10580192.html'

if __name__ == "__main__":
    print('<==========下载开始==========>', time.strftime('%Y-%m-%d %H:%M:%S'))
    spider_man = SpiderMan()
    # spider_man.crawl_image(image_url, 1)
    spider_man.crawl_image(academy_url, 2)
    print('<==========下载结束==========>', time.strftime('%Y-%m-%d %H:%M:%S'))
