import time
from URLManager import UrlManager
from Downloader import HtmlDownloader
from Parser import HtmlParser
from DataOutput import DataOutput


class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.manager2 = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl_image(self, start_url, total_page, __page=2):
        '''
        参数：
        :url 参数为需要下载的文章URL
        :total_page 大师板块下载页数
        :__page 扩展页数起始参数，用户请勿设定
        返回：
        无
        '''
        # 添加入口URL
        if 'image' in start_url or 'academy' in start_url:
            self.manager.add_new_url(start_url)
            # 判断url管理器中是否有新的url
            while(self.manager.has_new_url()):
                try:
                    # 从URL管理器获取新的url
                    new_url = self.manager.get_new_url()
                    # HTML下载器下载网页
                    html = self.downloader.download(new_url)
                    # 通过URL关键词判断是否是二级网页
                    if 'slide' in new_url:
                        # HTML解析器抽取网页数据
                        new_urls = self.parser.parse_data(html)
                        # 将抽取到url添加到URL管理器中
                        for url in new_urls:
                            print('地址+++>', url)
                        # self.self.manager2.add_new_url(new_urls)
                    else:
                        new_urls = self.parser.parse_urls(html)
                        for url in new_urls:
                            print('地址++>', url)
                        # self.manager.add_new_urls(new_urls)
                    # while(self.manager2.has_new_url()):
                    #     image_url = self.manager2.get_new_url()
                    #     data = self.downloader.download(image_url)
                    #     self.output.save_2_binary(title, data)
                    #     # 全部下载完成，增加去重标志
                    #     if not self.manager2.has_new_url():
                    #         self.manager2.add_duplication(title)
                    #         print('完成爬取==>', title)
                except Exception as e:
                    print('爬取失败==>', e)
            # 爬取后续页数
            if __page <= total_page:
                if 'image' in start_url:
                    next_url = '%s/index.php?action=getList&class_id=192&sub_classid=0&page=%s&not_in_id=' % (
                        start_url, str(__page))
                else:
                    next_url = '%s/index.php?action=getList&class_id=190&sub_classid=0&page=%s&not_in_id=' % (
                        start_url, str(__page))
                print('开始爬取==>第', str(__page), '页')
                return self.crawl_image(next_url, total_page, __page + 1)
        else:
            print('网址有错误，请检查')

        def crawl_bbs(self, start_url):
            '''
            参数：
            :url 参数为需要下载的文章URL，留空默认下载大师板块网页2页
            :total_page 大师板块下载页数
            :page 扩展页数参数，无需用户设定
            返回：
            无
            '''
            # 运行BBS下载程序
            if 'bbs' in start_url:
                url_base = start_url
                url_list = []
                page = 1
                html = self.downloader.download(url_base)
                doc = pq(html.text)
                total_page = doc('.page.module1200 span').text()

                if total_page:
                    total_page = int(re.sub("\D", "", total_page))
                else:
                    total_page = 1
                while page <= total_page:
                    url = url_base.replace(
                        '.html', '') + '_1_' + str(page) + '.html'
                    html = self.downloader.download(url)
                    results = self.parser.parse_data(html)
                    url_list = url_list + results['images']
                    page += 1
                url_list = {
                    'title': results['title'],
                    'images': url_list,
                }
                self.output.save_2_binary(url_list)
            else:
                print('网址有错误，请检查')

# 蜂鸟大师板地址
image_url = 'http://image.fengniao.com'
# 蜂鸟技法板地址
academy_url = 'http://academy.fengniao.com'
# 蜂鸟论坛帖子地址
bbs_url = 'http://bbs.fengniao.com/forum/10580192.html'

if __name__ == "__main__":
    print('<==========下载开始==========>', time.strftime('%Y-%m-%d %H:%M:%S'))
    spider_man = SpiderMan()
    spider_man.crawl_image(image_url, 2)
    spider_man.crawl_image(academy_url, 2)
    print('<==========下载结束==========>', time.strftime('%Y-%m-%d %H:%M:%S'))
