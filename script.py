#!/usr/bin/python3
# coding: utf-8
from bs4 import BeautifulSoup
import requests
import csv
from func import *
import sys

header = ['link', 'title', 'price', 'name', 'phone', 'time',
          'date', 'address', 'tags', 'content', 'ad_num', 'img']
html = requests.get(sys.argv[0])
soup = BeautifulSoup(html.content, 'lxml')
links = soup.findAll('td', class_='offer')
lst = []
for link in links:
    a = link.find('a')
    if a:
        lst.append(a.get('href'))
with open('olx.csv', 'w') as f:
    w = csv.writer(f)
    w.writerow(header)
    for link in lst:
        d = get_data(link)
        wlist = [d[i] for i in header]
        w.writerow(wlist)
