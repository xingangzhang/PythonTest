#!/usr/bin/python
# -*-coding:utf-8-*-

"""
@author: smartgang
@contact: zhangxingang92@qq.com
@file: baidu_nba.py
@time: 2017/12/1 18:18
"""
# !/usr/bin/python
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
import pickle
import os
import multiprocessing
import time


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
    def __init__(self, baseUrl, seeLZ, floorTag, total):
        self.baseUrl = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.pageIndex = 0
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.pages = []
        self.enable = False
        self.tool = Tool()
        self.file = None
        self.defaultFileName = u'baidu_t'
        self.floor = 1
        self.floorTag = floorTag
        self.totalPage = total
        self.failedPageList = []
        self.time = time.time()
    # 传入页码，获取该页帖子的代码
    def getPage(self, pageIndex):
        """
        :param pageIndex: page number
        :return: page code
        """
        try:
            url = self.baseUrl + '&pn=' + str(pageIndex * 50)
            if pageIndex is not 0:
                self.headers['Referer'] = self.baseUrl + '&pn=' + str(pageIndex - 1 * 50)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError, why:
            if hasattr(why, "reason"):
                print u"连接百度贴吧失败,错误原因", why.reason
                self.failedPageList.append(pageIndex)
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
        # repley number 0
        # link and content title 1 2
        # title author link and title author 3 4
        pattern = re.compile('<li class=" j_thread_list.*?' +
                             '<span class="threadlist_rep_num center_text".*?>(.*?)</span>.*?' +
                             '<div class="threadlist_title.*?<a href="(.*?)".*?>(.*?)</a>.*?' +
                             '<div class="threadlist_auth.*?<span class="frs-auth.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?' +
                             '<div class="threadlist_abs.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, pageContent)
        contents = []
        if items:
            for item in items:
                # content = self.tool.replace(item)
                contents.append([item[0].strip(), item[1].strip(), item[2].strip(), item[3].strip(), item[4].strip(),
                                 item[5].strip()])
                # print u"reply:%s  title link：%s content：%s author_link:%s author:%s content:%s" % (item[0], item[1], item[2], item[3], item[4], item[5])
            return contents
        else:
            return None

    def setFileName(self, title):
        if title is not None:
            self.file = open(title + ".txt", "w+")
        else:
            self.file = open(self.defaultFileName + ".txt", "w+")

    def writeData(self, contents, index):
        dir = 'f:\\python_data'
        if not os.path.exists(dir):
            os.mkdir(dir)  # 创建目录
            print('Successfully created directory', dir)
        file = dir + '\\' + str(index) + '.data'
        f = open(file, 'wb+')
        pickle.dump(contents, f)
        f.close()

    def start(self):
        try:
            print u"爬取第%d页" % self.pageIndex
            for i in range(1, int(self.totalPage) + 1):
                print u"正在写入第" + str(i) + u"页数据"
                pageContent = self.getPage(self.pageIndex)
                content = self.getPageContent(pageContent)
                self.writeData(content, self.pageIndex)
                self.pageIndex += 1
                # 出现写入异常
        except IOError, e:
            print u"写入异常，原因" + e.message
        finally:
            print u"写入任务完成"
    def doFail(self):
        if self.failedPageList:
            for item in self.failedPageList:
                print u"重新加载第" + str(item) + u"页数据"
                pageContent = self.getPage(self.pageIndex)
                content = self.getPageContent(pageContent)
                self.writeData(content, self.pageIndex)

    def doRun(self, index):
        try:
            print u"爬取第%d页" % index
            print u"正在写入第" + str(index) + u"页数据"
            pageContent = self.getPage(index)
            content = self.getPageContent(pageContent)
            self.writeData(content, index)
            # 出现写入异常
        except IOError, e:
            print u"写入异常，原因" + e.message
baseURL = 'https://tieba.baidu.com/f?kw=nba&ie=utf-8'
# baseURL = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
# seeLZ = raw_input("是否只获取楼主发言，是输入1，否输入0\n")
# floorTag = raw_input("是否写入楼层信息，是输入1，否输入0\n")
# bdtb = BDTB(baseURL, 1, 1)
# content = bdtb.getPage(0)
# # print content
# contents = bdtb.getPageContent(content)
# file = '1.data'
# f = open(file, 'wb+')
# pickle.dump(contents, f)
# f.close()
# del contents
#
# f = open(file, 'rb')
# stores = pickle.load(f)
# for s in stores:
#     print "%s" % s[5]
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
# file = 'F:\python_data\978.data'
# f = open(file, 'rb')
# stores = pickle.load(f)
# for s in stores:
#     print "%s" % s[2]
bdtb = BDTB(baseURL, 1, 1, 100)
def doRun(index):
    bdtb.doRun(index)
if __name__ == '__main__':
# bdtb.start()
    time1 = time.time()
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    for i in range(1, 170000, 1):
        result = pool.apply_async(doRun, (i, ))
    pool.close()
    pool.join()
    bdtb.doFail()
    time2 = time.time()
    print time2 - time1
