#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import datetime
import re
from bs4 import BeautifulSoup
def xinlang():
    k = 0
    def parselistlinks(url, time):
        try:
            res = requests.get(url, timeout=time)
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.text, 'html.parser')
            b = [a.select('a')[0]['href'] for a in soup.select('.list_009 li')]  # 每个分页的全部网页链接
            newsdetails = []
            nonlocal k
            for ent in b:
                k += 1
                print('新浪文件 %d 成功'%k)
                out = getnewsdetail(ent, 0.3)
                if out != {}:
                    newsdetails.append(out)
            for ent in errorArr:
                k += 1
                print('新浪文件 %d 成功' % k)
                out = getnewsdetail(ent, 1)
                if out != {}:
                    newsdetails.append(out)
            return newsdetails
        except BaseException:
            pass

    def getnewsdetail(newsurl, time):
        result = {}
        response = None
        try:
            response = requests.get(newsurl, timeout=time)
        except BaseException:
            errorArr.append(newsurl)
            return {}
        if response == None:
            return {}
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        if soup.select('#artibodyTitle'):
            result['title'] = soup.select('#artibodyTitle')[0].text
            result['time'] = soup.select('.time-source')[0].contents[0].strip()
            result['article'] = '\n'.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
            result['url'] = newsurl
        return result

    starttime = datetime.datetime.now()
    url = 'http://roll.news.sina.com.cn/news/gnxw/gdxw1/index_{}.shtml'
    news_total = []
    for i in range(1, 14):
        errorArr = []
        newsurl = url.format(i)
        newsary = parselistlinks(newsurl, 1)
        news_total.extend(newsary)
    print('新浪新闻总数为 %d' % (len(news_total)))
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    try:
        for m in news_total:
            name = 'sou1/新浪/' + re.sub(r, '', m['title']) + '.txt'
            with open(name, 'w', encoding='utf-8') as f:
                f.write(m['url'] + '\n')
                f.write(m['title'] + '\n')
                f.write(m['time'] + '\n')
                f.write('新浪\n')
                f.write(m['article'])
    except BaseException:
        pass
    endtime = datetime.datetime.now()

    print('新浪程序运行时间为 %d 秒' % ((endtime - starttime).seconds))
