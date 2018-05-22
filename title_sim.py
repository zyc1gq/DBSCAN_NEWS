#!/usr/bin/env python
# -*- coding: utf-8 -*-

#       实现个性化推荐的脚本

__author__ = 'ZYC@BUPT'
import random

import jieba
import sys
import json
jieba.load_userdict("E:/PYC/news-test/newword.dict")
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import math
import os

def Test2(rootDir):
    global title,mindic
    mindic=2
    title = {'title':'','url':''}
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if path.find(".json")!=-1:
            res=static(path)
            if res==-1:
                return 0
        if os.path.isdir(path):
            Test2(path)

def static(path):
    global title,mindic
    try:
        fp=open(path,"r")
        allstr=fp.read()
        new_dic=json.loads(allstr)
    except IOError:
        return 0
    for ne in new_dic['article']:
        segcont=[ostr]
        str_title=""
        seg_title = jieba.lcut(ne['title'], cut_all=True)
        for se in seg_title:
            str_title=str_title+" "+se
        segcont.append(str_title)
        global weight
        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(vectorizer.fit_transform(segcont))
        word = vectorizer.get_feature_names()  # 所有文本的关键字
        weight = tfidf.toarray()  # 对应的tfidf矩阵
        dis=dist(weight[0],weight[1])
        if dis < mindic and (ne['title'] in js_title)==False and dis>1.1:
            title['title']=ne['title']
            title['url']=ne['url']
            mindic=dis
        if mindic<=1.30:
            return -1

def dist(a, b):
    return math.sqrt(np.power(a - b, 2).sum())

global ostr,title,mindic
global js_title
title={}
js_title={}
ostr = sys.argv[1]
#ostr="专家汇聚把脉兰州牛肉拉面 献策打造“中华第一面”"
#ostr="最高法常务副院长：如何适用正当防卫制度...阿富汗总统加尼会见王毅...辽宁舰编队今日出海 将执行跨区机动训练任务"
ostr=ostr.replace("NULL","")
ostr=ostr.replace('[','["')
ostr=ostr.replace(']','"]')
arr=json.loads(ostr)
ostr=arr[0]
part=ostr.split("...")




for pa in part:
    seg_list = jieba.lcut(pa, cut_all=False)
    ostr = ""
    for se in seg_list:
        ostr = ostr + " " + se
    Test2("C:/xampp/htdocs/NewsFeed/json/tfidf")
    js_title[title['title']] = title['url']

count=len(js_title)

if count<10:
    file=os.listdir("C:/xampp/htdocs/NewsFeed/json/tfidf")
    while count<10:
        fil_len=len(file)
        em_pla=random.randint(0,fil_len-1)
        em_fp=open("C:/xampp/htdocs/NewsFeed/json/tfidf/"+file[em_pla],'r')
        em_str=em_fp.read()
        em_dic=json.loads(em_str)
        em_len=len(em_dic['article'])
        em_pla = random.randint(0, em_len - 1)
        js_title[em_dic['article'][em_pla]['title']] = em_dic['article'][em_pla]['url']
        count+=1
        em_fp.close()

re_str=json.dumps(js_title)
print(re_str)

