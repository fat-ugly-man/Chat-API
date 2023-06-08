#-*- coding:utf-8 -*-

import json
import requests
import time
import datetime
from elasticsearch import Elasticsearch
#es = Elasticsearch('http://172.23.29.106:9200', timeout=50000)
es = Elasticsearch(['http://192.168.101.113:9200'], timeout=50000, verify_certs=False)

def search_laws(key, title, max_len):
	body = {
		"query": {
			"match": {
				key : title
			}
		},
		"from": 0,
		"size": 10
	}
	res = es.search(index='law_answers_new', body=body)
	db_ret = [(item['_score'], item['_source']['question'], item['_source']['answer']) for item in res['hits']['hits']]
	ret_str = ''
	for item in db_ret:
		#ret_str += '问题：' + item[1] + ' 答案：' + item[2][:max_len].replace('\n', ' ')
		ret_str += str(item[0]) + '\t问题：' + item[1] + '\n'
	return ret_str

def gen_title():
	fout = open('question_data_format', 'w')
	fin = open('question_data', 'r')
	for line in fin:
		while True:
			title = line.strip().split('\t')[0]
			max_len = (3500 - len(title)) // 6
			laws_str = ''
			laws_str += search_laws('answer', title, max_len)
			laws_str +=search_laws('question', title, max_len)
			content = '"' + title + '" 请把以上内容总结改写成五个热门中文普法文章标题，每个标题的立场和角度尽量体现出内容的差别，不要同质化。每个标题占据一行。具体话题请参考以下的问题列表，筛选出你认为比较吸引人的话题，问答不一定与标题真的相关，所以不一定每一个问答都参考，仅参考你觉得相关的就可以：' + laws_str
			#print (content)
			#print ('========================')
			url = 'http://localhost:5888/bing/ask?style=creative&question=' + content
			ret_data = requests.get(url)
			res = json.loads(ret_data.content)
			if res['code'] == 200:
				ret_str = res['data']['answer'].replace('\n','\sb')
				ret_list = ret_str.strip().split('\sb')
				for item in ret_list[-5:]:
					print (item)
					print (item, file=fout)
				break
			else:
				print ('Error:{}'.format(res))
				time.sleep(30)
		time.sleep(5)
	fin.close()
	fout.close()

def expand_title(title):
	title = title + '，请找到这篇新闻或者新浪微博的热搜，并概括出主要内容。'
	url = 'http://localhost:5888/bing/ask?style=balanced&question=' + title
	ret_data = requests.get(url)
	res = json.loads(ret_data.content)
	if res['code'] == 200:
		print(res['data']['answer'])
	else:
		print ('Error:{}'.format(res))
	time.sleep(5)

gen_title()
exit(0)

day = datetime.datetime.now()
day_str = day.strftime('%Y-%m-%d')
with open('/Users/lwj/Documents/Dev/weibo-trending-hot-search/raw/' + day_str + '.json', 'r') as file:
	data = file.read()
	json_data = json.loads(data)

for item in json_data:
	#url = 'https://s.weibo.com/' + item['url']
	print (item['title'])
	expand_title(item['title'])
	#laws_str = search_laws('answer', item['title'], 10000)
	#print (laws_str)
