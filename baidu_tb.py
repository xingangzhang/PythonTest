#!/usr/bin/python
# -*-coding:utf-8-*-

"""
@author: smartgang
@contact: zhangxingang92@qq.com
@file: qs_crawl.py
@time: 2017/11/30 17:29
"""
import urllib
import urllib2
import re


class Tool:
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}| {6}')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n  ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()


class BDTB:
    def __init__(self, baseUrl, seeLZ, floorTag):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.pages = []
        self.enable = False
        self.tool = Tool()
        self.file = None
        self.defaultFileName = u'baidu_t'
        self.floor = 1
        self.floorTag = floorTag

    # 传入页码，获取该页帖子的代码
    def getPage(self, pageIndex):
        """
        :param pageIndex: page number
        :return: page code
        """
        try:
            url = self.baseUrl + self.seeLZ + '&pn=' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, why:
            if hasattr(why, "reason"):
                print u"连接百度贴吧失败,错误原因", why.reason
                return None

    def getPageReplyNum(self, pageContent):
        # <li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>
        pattern = re.compile('<li class="l_reply_num".*?><span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, pageContent)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, pageContent):
        pattern = re.compile('<li class="l_reply_num".*?><span.*?</span>.*?<span.*?>(.*?)</span>', re.S)
        result = re.search(pattern, pageContent)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageTitle(self, pageContent):
        pattern = re.compile('<h3 class=.*?>(.*?)</h3>')
        result = re.search(pattern, pageContent)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageContent(self, pageContent):
        pattern = re.compile('<div id="post_content.*?>(.*?)</div>')
        items = re.findall(pattern, pageContent)
        contents = []
        if items:
            for item in items:
                content = "\n" + self.tool.replace(item) + "\n"
                contents.append(content.encode('utf-8'))
            return contents
        else:
            return None

    def setFileName(self, title):
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultFileName + ".txt", "w+")

    def writeData(self, contents):
        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(
                    self.floor) + u"-----------------------------------------------------------------------------------------\n"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum(indexPage)
        title = self.getPageTitle(indexPage)
        self.setFileName(title)
        if pageNum == None:
            print u"URL已经失效，请重试"
            return
        try:
            print u"该帖子共有" + str(pageNum) + u"页"
            for i in range(1, int(pageNum) + 1):
                print u"正在写入第" + str(i) + u"页数据"
                page = self.getPage(i)
                contents = self.getPageContent(page)
                self.writeData(contents)
                # 出现写入异常
        except IOError, e:
            print u"写入异常，原因" + e.message
        finally:
            print u"写入任务完成"

print u"请输入帖子代号"
baseURL = 'http://tieba.baidu.com/p/3138733512'
# baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
# seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
# floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
bdtb = BDTB(baseURL, 1, 1)
bdtb.start()
# tool = Tool()
# baseURL = 'http://tieba.baidu.com/p/3138733512'
# bdtb = BDTB(baseURL, 1)
# file = open(r"F:\netcrawl\1.html", "w")
# contents = []
# content = bdtb.getPage(1)
# contents.append(content.encode('utf-8'))
# file.writelines(contents)
# print bdtb.getPageReplyNum(content)
# print bdtb.getPageNum(content)
# print bdtb.getPageTitle(content)
# print tool.replace(bdtb.getPageContent(content)[5])
