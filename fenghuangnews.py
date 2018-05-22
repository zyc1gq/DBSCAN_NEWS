#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import datetime
import re
from bs4 import BeautifulSoup
def fenghuang():
    starttime = datetime.datetime.now()
    k = 0
    def parselistlinks(url, time):
        try:
            res = requests.get(url,timeout=time)

            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text,'html.parser')
            b = [ent.select('a')[0]['href'] for ent in soup.select('.newsList ul li')]  # 每个分页的全部网页链接


            newsdetails = []
            nonlocal k
            for ent in b:
                k += 1
                print('凤凰文件 %d 成功' % k)
                out = getnewsdetail(ent, 0.3)
                if out != {}:
                    newsdetails.append(out)
            for ent in errorArr:
                k += 1
                print('凤凰文件 %d 成功' % k)
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
        html_str = response.text
        if len(html_str.split("<!--mainContent begin-->")) != 1:
            html_str = html_str.split("<!--mainContent begin-->")[1]
            if len(html_str.split("<!--mainContent end-->")[0]) != 1:
                html_str = html_str.split("<!--mainContent end-->")[0]
            else:
                return result
        else:
            return result
        soupa = BeautifulSoup(html_str,'html.parser')

        html_str = soupa.select('p')
        str = ''
        for i in html_str:
            if i.text != '':
                str = str + i.text + '\n'
        soup = BeautifulSoup(response.text,'html.parser')
        result['title'] = soup.select('#artical_topic')[0].text
        result['time'] = soup.select('.ss01')[0].text
        result['article'] = str
        result['url'] = newsurl
        return result

    starttime = datetime.datetime.now()
    url = 'http://news.ifeng.com/listpage/11502/20170630/{}/rtlist.shtml'
    news_total = []
    for i in range(1,10):
        errorArr = []
        newsurl = url.format(i)
        newsary = parselistlinks(newsurl,1)
        if newsary:
            news_total.extend(newsary)
    print('凤凰新闻总数为 %d' % (len(news_total)))
    r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    try:
        for m in news_total:
            name = 'sou1/凤凰网/' + re.sub(r, '', m['title'])+'.txt'
            with open(name, 'w',encoding='utf-8') as f:
                f.write(m['url']+'\n')
                f.write(m['title']+'\n')
                f.write(m['time']+'\n')
                f.write('凤凰网\n')
                f.write(m['article'])
    except BaseException:
        pass
    endtime = datetime.datetime.now()

    print('凤凰程序运行时间为 %d 秒' % ((endtime - starttime).seconds))
