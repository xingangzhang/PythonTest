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


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = 'https://www.qiushibaike.com/hot/page' + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, why:
            if hasattr(why, "reason"):
                print u"连接糗事百科失败,错误原因", why.reason
                return None

    def getPageItem(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        #print pageCode
        if not pageCode:
            print u"页面加载失败......"
            return None
        pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>.*?<h2>(.*?)</h2>.*?</a>.*?' +
                             '<div.*?class="articleGender.*?>(.*?)</div>.*?' +
                             '<div.*?class="content.*?>.*?<span>(.*?)</span>.*?</div>.*?</a>.*?' +
                             '(.*?)<div class="stats.*?>', re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        for item in items:
            haveImg = re.search("img", item[3])
            if not haveImg:
                pageStories.append([item[0].strip(), item[1].strip(), item[2].strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItem(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"第%d页\t发布人:%s\n%s\n" %(page,story[0],story[2])

    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"
        self.enable = True
        self.loadPage()
        newPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                newPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, newPage)

spider = QSBK()
spider.start()