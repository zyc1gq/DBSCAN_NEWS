#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xinlangnews
import fenghuangnews
import zhongguonews
import test_list
import time

site_first=site_sec=site_thir=0
print("请选择要爬取的网站:1代表爬取，0代表不爬取")
site_first=int(input("中国新闻网："))
site_sec=int(input("新浪新闻网："))
site_thir=int(input("凤凰新闻网："))


while True:
    start = time.clock()
    if site_first == 1:
        zhongguonews.zhongguoxinwen()
    if site_sec == 1:
        xinlangnews.xinlang()
    if site_thir == 1:
        fenghuangnews.fenghuang()
    test_list.dbs()
    end = time.clock()
    print(end-start)
    time.sleep(600)
