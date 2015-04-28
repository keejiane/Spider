# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib
import urllib2
import re
import os

class Tools(object):
	removeImg = re.compile('<img.*?>| {1,7}|&nbsp;')
	removeAddr = re.compile('<a.*?>|</a>')
	replaceLine = re.compile('<tr>|<div>|</div>|</p>')
	replaceTd = re.compile('<td>')
	replaceP = re.compile('<p.*?>')
	replaceBR = re.compile('<br><br>|<br>')
	removeExtra = re.compile('<.*?>')
	removeNoneLine = re.compile('\n+')

	def replace(self,p):
		p = re.sub(self.removeImg,'',p)
		p = re.sub(self.removeAddr,'',p)
		p = re.sub(self.replaceLine,'\n',p)
		p = re.sub(self.replaceTd,'\t',p)
		p = re.sub(self.replaceP,'\n    ',p)
		p = re.sub(self.replaceBR,'\n',p)
		p = re.sub(self.removeExtra,'',p)
		p = re.sub(self.removeNoneLine,'\n',p)
		return p.strip()

class TaoBao(object):

	def __init__(self):
		self.sitUrl = 'http://mm.taobao.com/json/request_top_list.htm'
		self.tool = Tools()

	def getPage(self,pageIndex):
		url = self.sitUrl + "?page=" + str(pageIndex)
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		return response.read().decode('gbk')

	def getContents(self,pageIndex):
		page = self.getPage(pageIndex)
		pattern = re.compile('<div class="list-item".*?pic-word.*?<a href="(.*?)".*?<img src="(.*?)".*?' +
			'<a class="lady-name.*?>(.*?)</a>.*?<strong>(.*?)</strong>.*?<span>(.*?)</span>',re.S)
		contents = re.findall(pattern,page)
		return contents

	def getDetailPage(self,infoUrl):
		response = urllib2.urlopen(infoUrl)
		return response.read().decode('gbk')

	def getBrief(self,page):
		patternInfo = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
		result = re.search(patternInfo,page)
		return self.tool.replace(result.group(1))

	def getAllImg(self,page):
		pattern = re.compile('<div class="mm-aixiu-content".*?>(.*?)<!--',re.S)
		content = re.search(pattern,page)
		patternImg = re.compile('<img.*?src="(.*?)"',re.S)
		images = re.findall(patternImg,content.group(1))
		return images

	def saveBrief(self,contents,name):
		fileName = name + "/" + name + ".txt"
		f = open(fileName,"w+")
		print u"正在写入她的信息为",fileName
		f.write(contents.encode('utf-8'))
		f.close()

	def saveImages(self,images,name):
		num = 1
		print u"发现",name,u"共有",len(images),u"张照片"
		for imageUrl in images:
			fileType = imageUrl.split(".").pop()
			if len(fileType) > 3:
				fileType = "jpg"
			fileName = name + "/" + str(num) + "." + fileType
			openImageUrl = urllib.urlopen(imageUrl)
			data = openImageUrl.read()
			f = open(fileName,"wb")
			f.write(data)
			print u"正在悄悄地保存一张图片为",fileName
			f.close()
			num += 1

	def mkdir(self,mpath):
		mpath = mpath.strip()
		isExists = os.path.exists(mpath)
		if not isExists:
			print u"正在偷偷创建一个为",mpath,u"的文件夹"
			os.makedirs(mpath)
			return True
		else:
			print u"名为",mpath,'的文件夹已经创建成功'
			return False

	def savePageInfo(self,pageIndex):
		contents = self.getContents(pageIndex)
		for item in contents:
			print u"发现一位模特,名字叫",item[2],u"芳龄",item[3],u",她在",item[4]
			print u"正在偷偷地保存",item[2],u"的信息"
			print u"又意外地发现她的个人地址是",item[0]
			detailUrl = item[0]
			detailPage = self.getDetailPage(detailUrl)
			brief = self.getBrief(detailPage)
			images = self.getAllImg(detailPage)
			self.mkdir(item[2])
			self.saveBrief(brief,item[2])
			self.saveImages(images,item[2])

	def savePagesInfo(self,start,end):
		for i in range(start,end):
			print u"正在偷偷寻找第",i,u"个地方，看看MM们在不在"
			self.savePageInfo(i)   	


tbMM = TaoBao()
tbMM.savePagesInfo(3,4)

