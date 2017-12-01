import urllib2
import urllib
import bs4

from bs4 import BeautifulSoup

values = {}
values['username'] = '32584932@qq.com'
values['password'] = 'zxg19911023'
data = urllib.urlencode(values)
url = "http://passport.csdn.net/account/login"
geturl = url + '?' + data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
# print response.read()
# print response.headers
html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

soup = BeautifulSoup(html)
# print soup.prettify()
print soup.name
del soup.a['class']
print soup.a
print soup.a.string
print soup.a.string
print soup.attrs
print type(soup.name)
print type(soup.p.string)
if type(soup.a.string)==bs4.element.Comment:
    print "is comment"

print soup.head.contents[0]
print soup.head.children
for child in soup.body.children:
    print child