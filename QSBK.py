# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import re

pages = raw_input("How many pages do you want to scrap:")
for page in range(1,int(pages)):
	url = 'http://www.qiushibaike.com/hot/page/' + str(page)
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
	header = {'User-Agent':user_agent}
	try:
		request = urllib2.Request(url,headers = header)
		response = urllib2.urlopen(request)
		content = response.read().decode('utf-8')
		pattern = re.compile('<div.*?class="author.*?>.*?<a.*?</a>.*?<a.*?>(.*?)</a>.*?<div.*?class' + 
		                 '="content".*?title="(.*?)">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>',re.S)
		items = re.findall(pattern,content)
		for item in items:
			haveImg = re.search('img',item[3])
			if not haveImg:
				print item[0],item[1],item[2],item[4]
	except urllib2.URLError,e:
		if hasattr(e,'code'):
			print e.code
		if hasattr(e,'reason'):
			print e.reason