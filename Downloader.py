import requests


class HtmlDownloader(object):

    # 网络请求相关参数
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
        'AppleWebKit/537.36 (KHTML, like Gecko) ' +
        'Chrome/67.0.3396.99 Safari/537.36',
        'Cookie': 'iamasmartboy',
    }
    params = {}
    data = {}

    def download(self, url, headers=headers, params=params, data=data):
        '''
        请求函数，使用requests库，已实现get和post
        :parameter:
        url 爬取的目标URL
        headers 所需头文件
        params get请求所需参数
        data post请求所需表单
        :return:
        正常时，Response对象。异常时，打印异常说明，返回None
        '''
        try:
            if not data:
                r = requests.get(url, headers=headers, params=params)
            else:
                r = requests.post(url, headers=headers, data=data)
            # 判断请求是否成功
            if r.status_code == 200:
                return r
            return None
        except requests.RequestException as e:
            # 打印请求错误说明
            print('请求错误==>', e.args)
            return None


if __name__ == '__main__':
    test = HtmlDownloader()
    print(test.download('https://httpbin.org/'))
