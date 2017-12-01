dic = {'aaa': 1, 'bbb': 2, 'ccc': 3}
print dic['aaa']
print dic['bbb']
dic['ccc'] = 10
if 'ccc' in dic:
    print dic['ccc']
print dic.get('ccc')
print dic.get('ddd')
if dic.get('ddd') == None:
    print 'None yes'
dic.pop('ccc')
print dic.get('ccc')
dictemp = dic.copy()
print dictemp['aaa']
dictemp['aaa'] = 100
print "now dictemp aaa is %d" % dictemp['aaa']
print "now dic aaa is %d" % dic['aaa']
print "Now dict length is %d" % len(dic)
# dic.clear()

print "End dict length is %d" % len(dic)
print "Value :%s" % dic.items()
print dic.has_key('aaa')
print dic.keys()
list_key = dic.keys()
print type(list_key)
dic.setdefault('ccc')
print dic.get('ccc')
dic.pop('aaa')
print str(dic)
dic.setdefault('ddd', 20)
dic.popitem()
print str(dic)
