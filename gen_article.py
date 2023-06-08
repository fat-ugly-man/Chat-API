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
		"size": 3
	}
	res = es.search(index='law_answers_new', body=body)
	db_ret = [(item['_score'], item['_source']['question'], item['_source']['answer']) for item in res['hits']['hits']]
	ret_str = ''
	for item in db_ret:
		ret_str += '\n问题：' + item[1] + '\n答案：' + item[2][:max_len]
		#ret_str += '问题：' + item[1] + '\n'
	return ret_str

day = datetime.datetime.now() + datetime.timedelta(days=1)
day_str = day.strftime('%Y%m%d')

back_words = ['sorry', 'mistake', 'diff']
with open('article_out_' + day_str, 'a') as fout:
	fin = open('question_data_format', 'r')
	for line in fin:
		flag = False
		title = line.strip().split('\t')[0]
		max_len = (3200 - len(title)) // 6
		laws_str = ''
		laws_str += search_laws('answer', title, max_len)
		laws_str +=search_laws('question', title, max_len)
		while True:
			content = title + ' 请使用前面这个标题，文章内容要尽量多包含用户搜索热度词且文章通俗易懂。我的这篇文章需要营造用户焦虑，引发用户的好奇心或者对自身状况的担忧，然后在当前平台上寻求律师的在线咨询帮助，平台的名称是LawyerGPT，平台的网站是www.lawyergpt.com.cn，不要在文章中出现平台的联系电话，也不要引导用户去任何APP。结合上面的内容，请生产出一篇合适的文章标题，并生成内容，内容字数控制到800字左右，尽量不和之前生产的文章重复。回答的格式为：标题：XXX。内容正文：XXX。内容必须以 感谢大家的支持 这句话结尾。我会给你提供一些真实的律师和用户的问答，请你作为参考，尽量包含这些问答中的关键词。如果你觉得问答与标题不相关，也可以忽略。请不要编造完全不存在的人和事。' + laws_str
			url = 'http://localhost:5888/bing/ask?style=creative&question=' + content
			#url = 'http://localhost:5888/bing/ask?style=balanced&question=' + content
			ret_data = requests.get(url)
			res = json.loads(ret_data.content)
			if res['code'] != 200:
				print ('Error:{}'.format(res))
				time.sleep(30)
				continue
			if 'sorry' in res['data']['answer'].lower() or 'mistake' in res['data']['answer'].lower() or 'topic' in res['data']['answer'].lower():
				print (res['data']['answer'].lower())
				time.sleep(5)
				break
			token = res['data']['token']
			print (res['data']['answer'].replace('\n','\sb'), end='', file=fout)
			print (res['data']['answer'].replace('\n','\sb'), end='')
			print (token)
			if '感谢大家' in res['data']['answer']:
				print ('', file=fout)
				print ('')
				time.sleep(5)
				break
		
			while True:
				time.sleep(5)
				content = '继续上一个回答的内容，写完这篇文章'
				url = 'http://localhost:5888/bing/ask?style=creative&question=' + content
				#url = 'http://localhost:5888/bing/ask?style=balanced&question=' + content
				url += '&token=' + token
				ret_data = requests.get(url)
				res = json.loads(ret_data.content)
				if res['code'] == 200:
					if 'sorry' in res['data']['answer'].lower() or 'mistake' in res['data']['answer'].lower() or 'topic' in res['data']['answer'].lower():
						flag = True
						break
					print (res['data']['answer'].replace('\n','\sb'), end='', file=fout),
					print (res['data']['answer'].replace('\n','\sb'), end='')
					token = res['data']['token']
					if '感谢大家' in res['data']['answer']:
						flag = True
						break
				else:
					print ('Error:{}'.format(res))
					time.sleep(30)
					break
			if flag:
				print ('', file=fout)
				print ('')
				time.sleep(5)
				break
	fin.close()
