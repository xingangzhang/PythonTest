#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
@author: smartgang

@contact: zhangxingang92@qq.com

@file: first_crawl.py

@time: 2017/11/29 14:34
"""
import urllib2
import urllib
import re

page = 1
url = 'https://www.qiushibaike.com/hot/page' + str(page)
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
headers = {}
headers['User-Agent'] = user_agent
try:
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    # print response.read()
    # pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class' +
    #                      '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',
    #                      re.S)
    content = response.read().decode('utf-8')
    print content
    # pattern = re.compile(r'<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>' +
    #                      r'.*?<div.*?class="articleGender.*?>(.*?)</div>.*?<div.*?class="content.*?>(.*?)</div>',
    #                      re.S)
    pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>.*?<h2>(.*?)</h2>.*?</a>.*?' +
                         '<div.*?class="articleGender.*?>(.*?)</div>.*?' +
                         '<div.*?class="content.*?>.*?<span>(.*?)</span>.*?</div>.*?</a>.*?' +
                         '(.*?)<div class="stats.*?>', re.S)

    items = re.findall(pattern, content)
    for item in items:
        haveImg = re.search("img", item[3])
        if not haveImg:
            print item[0], item[1], item[2]
except urllib2.URLError, why:
    if hasattr(why, "code"):
        print why.code
    if hasattr(why, "reason"):
        print why.reason
