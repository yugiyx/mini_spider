import requests


class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None


# 用户参数，CLI或GUI在此导入参数
image_start_url = 'http://image.fengniao.com'
bbs_start_url = 'http://bbs.fengniao.com/forum/10580192.html'
# 非用户直接设置参数
headers = {
    'Cookie': 'iamasmartboy',
}


def request_url(url, headers=None, params=None, data=None):
    '''
    请求函数，使用requests库。已实现get和post
    参数：
    :url 爬取的目标URL
    :headers 所需头文件
    :params get请求所需参数
    :data post请求所需表单
    返回：
    正常时，Response对象。异常时，打印异常说明,返回None
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
        print('请求错误==>', e.args)
        return None
