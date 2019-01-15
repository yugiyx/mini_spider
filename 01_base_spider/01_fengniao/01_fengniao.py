# 导入内置库
import re
import os
import shutil
import time
# 导入第三方库
import fire
import requests
from pyquery import PyQuery as pq


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


def parse_index(html):
    '''
    第一级解析函数，获取需要下载的文章URL
    参数：
    :html 请求函数得到的Response对象
    返回：
    文章未下载，文章URL列表。文章下载过，打印重复说明,返回None
    '''
    if html:
        doc = pq(html.text)
        if doc('title'):
            items = doc('.main .listBox').find('.pic.pic75')
            for item in items.items():
                title = item.attr('title').replace('|', '').strip()
                lis = item.attr('href')
                # 通过判断url是否含有slide，去掉非画廊内容
                if 'slide' in lis:
                    yield remove_duplication(title, lis)
        else:
            doc = html.json().get('data')
            for item in doc:
                title = item.get('title').replace('|', '').strip()
                lis = item.get('url')
                if 'slide' in lis:
                    yield remove_duplication(title, lis)


def parse_document(html):
    '''
    第二级解析函数，获取需要文章内部资源地址
    参数：
    :html 请求函数得到的Response对象
    返回：
    文章标题
    内部图片URL列表
    '''
    if html:
        doc = pq(html.text)
        if 'image' in html.url:
            title = doc('title').text().replace(
                '_组图-蜂鸟网', '').replace('|', '').strip()
            html = doc('html').html().replace('\\', '')
            results = re.findall(r'pic_url":"(.*?)","pic_url_s', html, re.S)
        elif 'bbs' in html.url:
            title = doc('title').text().replace('【有图】', '').strip()
            html = doc('.postMain.module1200').html()
            results = re.findall(
                r'class="img".*?src="(.*?)"/></a>', html, re.S)
        url_list = {
            'title': title,
            'images': results,
        }
        return url_list


def remove_duplication(title, lis):
    '''
    去重判断，这里查询的清单，是后续下载成功后写入的标题
    参数：
    :title 文章标题
    :lis URL列表
    返回：
    文章未下载，文章URL列表。文章下载过，打印重复说明,返回None
    '''
    with open('download_log.txt', 'r', encoding='utf-8') as f:
        if not (title in f.read()):
            print('获得==>' + title)
            print('地址==>' + lis)
            return lis
        else:
            print('已存在，无需下载==>' + title)
            return None


def save_to_disk(url_list, folder='image'):
    '''
    存储二进制文件，并记录去重标志位
    参数：
    :url_list 下载清单列表list
    返回：
    无
    '''
    title = url_list['title']
    url_list = url_list['images']
    # 以当前日期和标题建立文件夹
    path = folder + '/' + time.strftime('%Y%m%d') + '/' + title
    try:
        os.makedirs(path)
    except FileExistsError:
        print('删除已存在目录')
        # 递归删除目录和目录里面的文件
        shutil.rmtree(path)
        os.makedirs(path)
    print('开始下载==>')
    for index, url in enumerate(url_list):
        print(index + 1, '==>', url)
        file_path = path + '/' + str(index + 1) + '.jpg'
        r = request_url(url)
        with open(file_path, 'wb') as f:
            f.write(r.content)
    if folder == 'image':
        # 去重判断标志，全部下载完成以后才会添加到清单，没有下载完的文章，不会记录标志位
        with open('download_log.txt', 'a', encoding='utf-8') as f:
            print('成功下载==>', title)
            f.write(title + '\n')
    else:
        print('成功下载==>', title)


def main(url=image_start_url, page=2, total_page=2):
    '''
    参数：
    :url 参数为需要下载的文章URL，留空默认下载大师板块网页2页
    :page 此参数为程序初始参数，请勿使用
    :total_page 大师板块下载页数
    返回：
    无
    '''
    # 运行大师板块下载程序
    if 'image' in url:
        html = request_url(url, headers)
        for url in parse_index(html):
            if url:
                html = request_url(url, headers)
                url_list = parse_document(html)
                save_to_disk(url_list)
        if page <= total_page:
            next_url = image_start_url + \
                '/index.php?action=getList&class_id=192&sub_classid=0&page=' +\
                str(page) + '&not_in_id='
            print('开始爬取==>第', str(page), '页')
            return main(next_url, page + 1, total_page)
    # 运行BBS下载程序
    elif 'bbs' in url:
        url_base = url
        url_list = []
        page -= 1
        html = request_url(url_base, headers)
        doc = pq(html.text)
        total_page = doc('.page.module1200 span').text()

        if total_page:
            total_page = int(re.sub("\D", "", total_page))
        else:
            total_page = 1
        while page <= total_page:
            url = url_base.replace('.html', '') + '_1_' + str(page) + '.html'
            html = request_url(url, headers)
            results = parse_document(html)
            url_list = url_list + results['images']
            page += 1
        url_list = {
            'title': results['title'],
            'images': url_list,
        }
        save_to_disk(url_list, 'bbs')
    else:
        print('参数为需要下载的文章URL，留空默认下载大师板块网页2页')


if __name__ == '__main__':
    print('<==========下载开始==========>', time.strftime('%Y-%m-%d %H:%M:%S'))
    # main(bbs_start_url)
    fire.Fire(main)
    print('<==========下载结束==========>', time.strftime('%Y-%m-%d %H:%M:%S'))
