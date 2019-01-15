# 轻量化爬虫框架

## 0x01 轻量化爬虫的意义
如果能用最简单的方法（小型库组合）实现需求，就无需使用更复杂的方法。杀鸡焉用牛刀（scrapy）

### 特点：
1. 代码结构清晰，容易理解，便于技术交流
2. 依赖库少，容易布署
3. 使用fire和pyinstall制作成命令行和打包成可执行软件，体积非常小巧。供非程序员使用

### 缺点：
1. 通用性差，可能需要同时修改多处模块。而不是仅仅修改解析模块
2. 无法短时间爬取海量数据，性能不够强大
2. 容错性差

## 0x02 轻量爬虫架构
### 框架图
![image](https://github.com/yugiyx/my_spider/blob/master/01_base_spider/readme_pic/snap-01.png?raw=true)

### 爬虫调度器
1. 主要负责统筹其他四个模块的协调工作

### URL管理器
1. URL链接，维护已经爬取和未爬取的URL
2. 提供获取新URL链接的接口

### HTML下载器
1. 从URL管理器中获取未爬取URL
2. 下载URL内容

### HTML解析器
1. 从HTML下载器获取已经下载的网页，从中解析出新的URL返回URL管理器
2. 将有效数据传给数据存储起

### 数据存储器
1. 以某种需要的形式存储有效数据
2. 存储增量爬虫所需要的历史爬取记录，用于去重复

### 爬虫运行流程
![image](https://github.com/yugiyx/my_spider/blob/master/01_base_spider/readme_pic/snap-02.png?raw=true)

## 0x03 程序环境
### Python及相关第三方库
* `python3.7.2`     python解析器
* `requests 2.20.1` 请求库
* `pyquery 1.4.0`   解析库
* `pymongo 3.7.2`   MongoDB库
* `fire 0.1.3 `     命令行制作库
* `PyInstaller 3.4` 可执行程序打包库

## 0x04 程序组件说明
* `SpiderMan.py`    爬虫调度器
* `URLManager.py`   URL管理器
* `Downloader.py`   HTML下载器
* `Parser.py`       HTML解析器
* `DataOutput.py`   数据存储器
* `Download_log.txt`下载历史记录(程序自动生成)

## 0x05 配置程序说明
具体看源代码内部注释

## 0x06 下一步计划
* CR: 优化代码，使程序更简洁优雅
* CR: 优化代码，增加通用度
* CR：增加多线程提供下载速度
* Fix：暂无

## 0x07 版本记录CHANGELOG

