#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'ZYC@BUPT'
import shutil
import jieba
import os
import sys
import json
import importlib,sys
importlib.reload(sys)
#reload(sys)
jieba.load_userdict("newword.dict")
#sys.setdefaultencoding("utf-8")
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import time
import numpy as np

from sklearn.cluster import DBSCAN


def Test2(rootDir):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        # print path.decode('gb2312')
        if path.find(".txt") != -1:
            Participle(path)
        if os.path.isdir(path):
            Test2(path)


def Participle(path):
    try:
        fp = open(path, "r", encoding="utf-8")
        ad = fp.readline().strip('\n')
        na = fp.readline().strip('\n')
        ti = fp.readline().strip('\n')
        si = fp.readline().strip('\n')
        cont = na + fp.read()
        fp.close()
    except IOError:
        return 0
    try:
        insi = {}
        insi['time'] = ti
        print (ti)
        insi['url'] = ad
        insi['title'] = na
        insi['site'] = si  # decode("gb2312").encode("utf-8")
        global fnum
        global segcont
        global doc
        seg_list = jieba.lcut(cont, cut_all=False)
        stline = ""
        for word in seg_list:
            if ((word in d) is False) and word != '\n':
                stline = stline + " " + word
        segcont.append(stline)
        print (str(fnum) + " 分词")
        doc[fnum] = insi
        fnum = fnum + 1
    except UnicodeError:
        return 0


def TFIDF():
    global segcont
    global weight
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(segcont))
    word = vectorizer.get_feature_names()  # 所有文本的关键字
    weight = tfidf.toarray()  # 对应的tfidf矩阵
    del segcont
    seg = []
    for i in range(len(weight)):
        enstr = ""
        for j in range(len(word)):
            if weight[i][j] >= 0.1:
                enstr = enstr + " " + word[j]
        seg.append(enstr)
    del weight
    global we
    vec = CountVectorizer()
    tra = TfidfTransformer()
    tidf = tra.fit_transform(vec.fit_transform(seg))
    wo = vec.get_feature_names()
    we = tidf.toarray()
    start = time.clock()

    from sklearn.cluster import DBSCAN
    db = DBSCAN(eps=1.24, min_samples=3).fit(we)###########################1.28   3


    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    end = time.clock()
    print (max(labels))
    print ('finish all in %s' % str(end - start))
    store(labels, max(labels))
    #tstore(labels, max(labels))
    # print len(labels)


def store(clusters, clusterNum):
    global doc
    fpath = "C:/xampp/htdocs/NewsFeed/json/tfidf/"
    i = 0
    di = []
    static = [0]
    stat_title = []
    while i <= clusterNum:
        static.append(0)
        di.append({'class': '0', 'ratio': 0.0, 'article': []})
        stat_title.append({})
        i += 1
    n = 0
    i = 1
    for cl in clusters:
        if cl != -1:
            di[cl]['article'].append(doc[i])
            enseg=jieba.lcut(doc[i]['title'], cut_all=False)
            for word in enseg:
                if ((word in d) is False) and word != '\n' and word!='"':
                    if  ((word in stat_title[cl]) is False):
                        stat_title[cl][word]=0
                    else:
                        stat_title[cl][word] += 1
            static[cl] += 1
            n += 1
        i += 1
    i = 0
    file = os.listdir("C:/xampp/htdocs/NewsFeed/json/tfidf/")
    for fi in file:
        pa=fpath+fi
        os.remove(pa)
    while i <= clusterNum:
        k = 0
        di[i]['class']=""
        res=sorted(stat_title[i].items(), key=lambda d: d[1], reverse=True)
        for re in res:
            if (len(re[0])>1)==True:
                di[i]['class']=di[i]['class']+" "+re[0]
                k+=1
            if (k>=2)==True:
                break
        di[i]['ratio'] = 1.0 * static[i] / n
        path = fpath + di[i]['class'] + ".json"
        jtemp = json.dumps(di[i])
        enfp = open(path, 'w')
        enfp.write(jtemp)
        i += 1
        enfp.close()



def tstore(clusters, clusterNum):  # 测试使用
    global doc
    fpath = "./test_res/"
    i = -1
    wr = []
    while i <= clusterNum:
        path = fpath + str(i) + ".txt"
        fp = open(path, 'w')
        wr.append(fp)
        i += 1
    i = 1
    for cl in clusters:
        enstr = ""
        enstr = doc[i]['title'] + doc[i]['url']
        wr[(cl + 1)].write(enstr + '\n')
        i += 1


def dbs():
    global fnum, doc, segcont, d
    fnum = 1
    segcont = []
    doc = {}
    stfp = open("stop.txt", "r")
    stcont = stfp.read()
    list_a = jieba.lcut(stcont, cut_all=False)
    d = set([])
    for li in list_a:
        d.add(li)
    stfp.close()
    Test2('./sou1')
    TFIDF()

