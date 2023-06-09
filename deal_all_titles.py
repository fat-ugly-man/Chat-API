#-*- coding:utf-8 -*-
import os

def create_files():
    fin = open('2023_hot_laws', 'r')
    for line in fin:
        items = line.strip().split('\t')
        if len(items[0]) != 4:
            continue
        filename = 'all_titles/' + items[0] + '_base'
        if not os.path.exists(filename):
            if len(items[0]) == 4:
                os.system('touch ' + filename)        
        fout = open(filename, 'a')
        print (line.strip(), file=fout)
        fout.close()
    fin.close()

#create_files()

def clean(filename):
    dic = {}
    fin = open('all_titles/通用_base', 'r')
    for line in fin:
        key = line.strip()
        dic[key] = 1
    fin.close()

    fin = open(filename, 'r')
    for line in fin:
        title = line.strip()
        for key in dic:
            if key in title:
                continue
        print (key)
    fin.close()

#clean('all_titles/侵权责任_expand')


def mix_base_data(num):
    from collections import defaultdict
    path = 'all_titles/'
    fnames = ['交通相关','侵权责任','刑事行政','司法程序','婚姻家庭','企业相关','债权债务','劳动纠纷','合同纠纷','房产征地']
    cur_num = 0
    data_dict = defaultdict(list)
    for fname in fnames:
        file_str = path + fname + '_base'
        fin = open(file_str, 'r')
        for line in fin:
            items = line.strip().split('\t')
            data_dict[fname].append(items[0] + '\t' + items[-2])
        fin.close()

    max_len = -1
    for key in data_dict:
        data_dict[key] = list(set(data_dict[key]))
        if len(data_dict[key]) > max_len:
            max_len = len(data_dict[key])

    mix_data = [[] for i in range(num)]
    for i in range(max_len):
        cur_num = i % num
        for fname in fnames:
            if len(data_dict[fname]) - 1 < i:
                continue
            mix_data[cur_num].append(data_dict[fname][i])

    for i in range(num):
        fout = open(path + 'mix_data_' + str(i), 'w')
        for line in mix_data[i]:
            print (line, file=fout)
        fout.close()

mix_base_data(2)
    
    
