# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import re

class Tool(object):
	removeImg = re.compile('<img.*?>| {7}|')
	removeAddr = re.compile('<a.*?>|</a>')
	replaceLine = re.compile('<tr>|<div>|</div>|</p>')
	replaceTd = re.compile('<td>')
	replaceP = re.compile('<p.*?>')
	replaceBR = re.compile('<br><br>|<br>')
	removeExtra = re.compile('<.*?>')

	def replace(self,p):
		p = re.sub(self.removeImg,'',p)
		p = re.sub(self.removeAddr,'',p)
		p = re.sub(self.replaceLine,'\n',p)
		p = re.sub(self.replaceTd,'\t',p)
		p = re.sub(self.replaceP,'\n    ',p)
		p = re.sub(self.replaceBR,'\n',p)
		p = re.sub(self.removeExtra,'',p)
		return p.strip()

class BDTB(object):
	def __init__(self, baseUrl, seeLz):
		self.baseUrl = baseUrl
		self.seeLz = '?see_lz=' + str(seeLz)
		self.tool = Tool()
		self.defaultTitle = u"百度贴吧"
		self.floor = 1
		self.file = None

	def getPage(self,pageNum):
		url = self.baseUrl + self.seeLz + '&np=' + str(pageNum)
		try:
			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
			return response.read().decode('utf-8')
		except urllib2.URLError,e:
			if hasattr(e,"code"):
				print e.code
			if hasattr(e,"reason"):
				print u"连接百度贴吧失败，错误原因：",e.reason

	def getTitle(self,page):
		pattern = re.compile('<h1 class="core_title_txt.*?>(.*?)</h1>',re.S)
		result = re.search(pattern,page)
		if result:
			return result.group(1).strip()
		else:
			return None

	def getPageNum(self,page):
		pattern = re.compile('<li class="l_reply_num.*?</span>.*?<span.*?>(.*?)</span>',re.S)
		result = re.search(pattern,page)
		if result:
			return result.group(1).strip()
		else:
			return None

	def getContent(self,page):
		pattern = re.compile('<div id="post_content_.*?>(.*?)</div>',re.S)
		items = re.findall(pattern,page)
		contents = []
		for item in items:
			content = "\n" + self.tool.replace(item) + "\n"
			contents.append(content.encode('utf-8'))
		return contents

	def setFileTitle(self,title):
		if title is not None:
			self.file = open(title + ".txt","w+")
		else:
			self.file = open(self.defaultTitle + ".txt","w+")

	def writeData(self,contents):
		for i in contents:
			floorLine = "\n" + str(self.floor) + u"------------------------------------------------------------------------------------------------\n"
			self.file.write(floorLine)
			self.file.write(i)
			self.floor += 1

	def start(self):
		indexPage = self.getPage(1)
		pageNum = self.getPageNum(indexPage)
		title = self.getTitle(indexPage)
		self.setFileTitle(title)
		if pageNum == None:
			print u"URL已失效，请重试"
			return
		try:
			print u"帖子共有" + str(pageNum) + u"页"
			for j in range(1,int(pageNum)+1):
				print u"正在写入第" + str(j) + u"页数据"
				page = self.getPage(j)
				contents = self.getContent(page)
				self.writeData(contents)
		except IOError,e:
			print u"写入异常，原因" + e.message
		finally:
			print u"写入任务成功"


print u"请输入贴吧帖子代号"
baseUrl = 'http://tieba.baidu.com/p/' + str(raw_input(u'http://tieba.baidu.com/p/'))
seeLz = raw_input(u"是否只获取楼主发言，是输入1，否输入0\n".encode("mbcs"))
bdtb = BDTB(baseUrl,seeLz)
bdtb.start()


		
