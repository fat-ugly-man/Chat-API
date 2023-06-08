#-*- coding:utf-8 -*-

import os, sys
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(CURRENT_DIR + '/../') 

from setting import *
from sqlalchemy import distinct
from elasticsearch import Elasticsearch

import datetime
import json
import requests
import time
import os
import re

def get_5118_content(content):
	url = 'http://apis.5118.com/wyc/seniorrewrite'
	headers = {
		'Authorization': '9461345B54054E6795DEC2742588A809',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
	}
	params = {
		'txt': content,
		'sim': 1
	}
	try:
		ret_data = requests.post(url, headers=headers, data=params)
		res = json.loads(ret_data.content)
	except:
		res = {'errmsg': '未知错误'}
	time.sleep(1)
	return res

def submit_baidu(urls, type_level):
	access_token = "24.beca8271c0f33552f3bc493f6a9d6893.2592000.1687597248.282335-32024263"
	url = "https://openapi.baidu.com/rest/2.0/smartapp/access/submitsitemap/api?access_token=" + access_token 
	data = {"type": type_level, "url_list": urls}  
	res = requests.post(url=url, data=data) 
	print('提交百度反馈：' + res.text)

def submit_bing(url_list):
	key = 'a45a91eb62dc4b14978fb21360080df3'
	url = 'https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch'
	headers = {
		'Host': 'ssl.bing.com',
		'Content-Type': 'application/json; charset=utf-8'
	}
	params = {
		'apikey': key
	}
	data = {
		'siteUrl': 'https://www.lawyergpt.com.cn',
		'urlList': url_list
	}
	res = {}
	try:
		ret_data = requests.post(url, json=data, headers=headers, params=params)
		res = json.loads(ret_data.content)
		print (res)
	except Exception as e:
		print (e)

def getcats(title):
	url = 'http://localhost:8000/siBuLabelRecognitionBatch'
	params = {
		'q': [title]
	}
	ret_data = requests.post(url, json=params)
	cat_res_list = json.loads(ret_data.content)
	cat1 = cat_res_list['data'][0]['one_level']['categoryName']
	cat2 = cat_res_list['data'][0]['two_level']['label']
	cat3 = str(cat_res_list['data'][0]['two_level']['specialId'])
	return cat1, cat2, cat3

from_day = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
to_day = datetime.datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
day_str = datetime.datetime.now().strftime('%Y%m%d')

fout = open('articles.txt', 'w')
fin = open('article_out_' + day_str, 'r')
for line in fin:
	if '内容正文：' not in line:
		continue
	if '标题：' not in line:
		continue
	while '感谢大家支持' in line:
		line = line.strip().split('感谢大家支持')[-1]
	text = line.strip().split('感谢大家支持')[0]
	text = re.sub(r'\\sb+', '\n', text)
	text = re.sub(r'\n+', '\n', text)
	text = text.replace('LawyerGPT.com.cn', 'www.lawyergpt.com.cn').replace('LawyerGPT.com', 'www.lawyergpt.com.cn')
	text = text.replace('www.LawyerGPT.com.cn', 'www.lawyergpt.com.cn').replace('www.LawyerGPT.com', 'www.lawyergpt.com.cn')
	aid = str(cur_id)
	source_url = 'https://www.lawyergpt.com.cn/article/' + aid + '.html'
	url = '/pages/index/article?content_id=' + aid
	title = text.split('内容正文：')[0].split('标题：')[-1]
	content = text.split('内容正文：')[-1]
	if len(content) < 200:
		continue
	if '抱歉' in content or '对不起' in content:
		end_content = content[-500:].split('抱歉')[0]
		content = content[:-500] + end_content
		end_content = content[-500:].split('对不起')[0]
		content = content[:-500] + end_content
		content = content + '只需访问www.lawyergpt.com.cn，就可以轻松找到适合您的律师，并与其进行在线沟通和协商。LawyerGPT平台保证您的隐私安全和信息保密，让您享受便捷、高效、优质的法律服务。'
	cat1, cat2, cat3 = getcats(title)
	
	print ('网页链接：' + source_url, file=fout)
	print ('小程序链接：' + url, file=fout)
	print ('标题：', file=fout)
	print (title.strip(), file=fout)
	print ('内容：', file=fout)
	print (content.strip(), file=fout)
	print ('===============================================================', file=fout)
fin.close()
fout.close()

