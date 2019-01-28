from URLManager import UrlManager
from Downloader import HtmlDownloader
from Parser import HtmlParser
from DataOutput import DataOutput


class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl_image(self, root_url, total_page, page=2):
        '''
        参数：
        :url 参数为需要下载的文章URL，留空默认下载大师板块网页2页
        :total_page 大师板块下载页数
        :page 扩展页数参数，无需用户设定
        返回：
        无
        '''
        # 运行大师板块下载程序
        if 'image' in root_url:
            html = self.downloader.download(root_url)
            for url in self.parser.parse_urls(html):
                if url:
                    html = self.downloader.download(url)
                    title, url_list = self.parser.parse_data(html)
                    self.output.save_2_binary(title, url_list)
                    self.manager.add_duplication(title)
            if page <= total_page:
                next_url = root_url + \
                    '/index.php?action=getList&class_id=192&sub_classid=0&page=' +\
                    str(page) + '&not_in_id='
                print('开始爬取==>第', str(page), '页')
                return self.crawl_image(next_url, page + 1, total_page)
        else:
            print('网址有错误，请检查')

        def crawl_bbs(self, root_url):
            '''
            参数：
            :url 参数为需要下载的文章URL，留空默认下载大师板块网页2页
            :total_page 大师板块下载页数
            :page 扩展页数参数，无需用户设定
            返回：
            无
            '''
            # 运行BBS下载程序
            if 'bbs' in root_url:
                url_base = root_url
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

image_start_url = 'http://image.fengniao.com'
bbs_start_url = 'http://bbs.fengniao.com/forum/10580192.html'

if __name__ == "__main__":
    spider_man = SpiderMan()
    spider_man.crawl_image(image_start_url, 2)
    spider_man.crawl_bbs(bbs_start_url)
