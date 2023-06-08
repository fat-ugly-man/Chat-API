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
        print (line, file=fout)
        fout.close()
    fin.close()

filename = 'all_titles/婚姻家庭_base'
fin = open(filename, 'r')

