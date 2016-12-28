#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import requests
import codecs

from bs4 import BeautifulSoup
from datetime import datetime

#获取评论总数
def getCommentsCount(newsurl):
	#文章评论请求链接，通过newsid来标识
	commentsurl = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8&page=1&page_size=20'

	newsid = re.search('doc-i(.*).shtml',newsurl).group(1)
	res = requests.get(commentsurl.format(newsid))
	if res.status_code == 200:
		jd = json.loads(res.text.strip('var data=').strip())
		return jd['result']['count']['total']
	else:
		return 0

#获取新闻详细内容
'''
标题、时间、来源、编辑、评论总数、内容
'''
def getDetail(newsurl):
	result = {}
	res = requests.get(newsurl)
	if res.status_code == 200:
		res.encoding = 'utf-8'
		soup = BeautifulSoup(res.text,'html.parser')
		result['title'] = soup.select('#artibodyTitle')[0].text
		#time_tmp = soup.select('.time-source')[0].contents[0].strip()
		#result['time'] = datetime.strptime(time_tmp,'%Y年%m月%d日%H:%M')
		result['time'] = soup.select('.time-source')[0].contents[0].strip()
		result['source'] = soup.select('.time-source span')[0].text
		result['editor'] = soup.select('.article-editor')[0].text.strip('责任编辑：')
		result['comments'] = getCommentsCount(newsurl)
		result['artile'] = ' '.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
	return result

#获取新浪国内新闻的链接地址url
def getUrls(urls):
	result = []
	res = requests.get(newsurl)
	res.encoding = 'utf-8'
	soup = BeautifulSoup(res.text,'html.parser')
	for a in soup.select('.news-item h2 a'):
		result.append(a['href'])
		
	return result

#结果以json格式保存到文件
def saveTofile(data):
	f = codecs.open(r'e:\pytest\sinanews.json','w+','utf-8')
	obj = json.dumps(data, ensure_ascii=False)
	f.write(obj)
	f.close()

#测试函数	
def test(newsurl):
	urls = getUrls(newsurl)
	print(len(urls))
	data = []

	for url in urls:
		r = getDetail(url)
		r['url'] = url
		data.append(r)

	if len(data)>0:	
		print('ok,done!')
		saveTofile(data)
	else:
		print('wrong somewhere...')
	
if __name__ == '__main__':
	#新浪新闻国内新闻url
	newsurl = 'http://news.sina.com.cn/china/'

	test(newsurl)