#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import datetime
import re
from bs4 import BeautifulSoup
def zhongguoxinwen():
    k = 0
    def parselistlinks(url, time):
        try:
            res = requests.get(url,timeout=time)
            res.encoding = 'gbk'
            soup = BeautifulSoup(res.text,'html.parser')
            b = ['http://'+ent.select('a')[0]['href'].lstrip('//') for ent in soup.select('.content_list ul li .dd_bt')]#每个分页的全部链接
            newsdetails = []
            nonlocal k
            for ent in b:
                k += 1
                print('中国新闻文件 %d 成功' % k)
                out = getnewsdetail(ent, 0.3)
                if out != {}:
                    newsdetails.append(out)
            for ent in errorArr:
                k += 1
                print('中国新闻文件 %d 成功' % k)
                out = getnewsdetail(ent, 1)
                if out != {}:
                    newsdetails.append(out)

            return newsdetails

        except BaseException:
            pass

    def getnewsdetail(newsurl,time):
        result = {}
        response = None
        try:
            response = requests.get(newsurl, timeout=time)
        except BaseException:
            errorArr.append(newsurl)
            return {}
        if response == None:
            return {}
        response.encoding = 'gbk'
        soup = BeautifulSoup(response.text,'html.parser')
        if soup.select('#cont_1_1_2 h1'):
            result['title'] = soup.select('#cont_1_1_2 h1')[0].text.strip()
            result['time'] = soup.select('.left-t')[0].contents[0].rstrip('来源：').strip()
            result['article'] = '\n'.join([p.text.strip() for p in soup.select('.left_zw p')])
            result['url'] = newsurl
        return result

    starttime = datetime.datetime.now()
    url = 'http://www.chinanews.com/scroll-news/news{}.html'
    news_total = []
    for i in range(1,6):
        errorArr = []
        newsurl = url.format(i)
        newsary = parselistlinks(newsurl,1)
        news_total.extend(newsary)
    print('中国新闻新闻总数为 %d' % (len(news_total)))
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    for m in news_total:
        try:
            name = 'sou1/中国新闻网/' + re.sub(r, '', m['title']) + '.txt'
            with open(name, 'w', encoding='utf-8') as f:
                f.write(m['url'] + '\n')
                f.write(m['title'] + '\n')
                f.write(m['time'] + '\n')
                f.write('中国新闻网\n')
                f.write(m['article'])
        except BaseException:
            pass
    endtime = datetime.datetime.now()

    print('中国新闻程序运行时间为 %d 秒' % ((endtime - starttime).seconds))
