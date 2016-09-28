#!/usr/bin/python3
# coding: utf-8
from bs4 import BeautifulSoup
import re
import requests
import csv
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}


def get_phone(url):
    ''' get phone number from given link '''
    uid = re.findall(r'-ID(.*?).html', url)[0]
    r = requests.get('http://olx.ua/ajax/misc/contact/phone/' + uid)
    phones = re.findall(r'([ 0-9]+)', r.text)
    return [s for s in phones if s != ' ']


def get_data(url):
    ''' collect all data in dict '''
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, 'lxml')
    data = {}
    data['title'] = soup.find('h1').text.strip()
    data['price'] = soup.find('strong', class_='xxxx-large').string
    data['address'] = soup.find('strong', class_='c2b small').string.strip()
    adr = soup.find('small', class_='c62').text.split(',')
    data['time'] = re.findall(r'[0-9]{2}:[0-9]{2}', adr[0])[0]
    data['date'] = adr[1].strip()
    data['ad_num'] = re.findall(r'[0-9]+', adr[2])[0]
    a = soup.find(class_='userdetails').findChildren('span')
    x, y = [s.text for s in a[:2]]
    data['name'] = x + ' ' + y
    tds = soup.find('table', class_='details').find_all('table', class_='item')
    data['tags'] = [' '.join(t.text.split()) for t in tds]
    data['content'] = soup.find('div', id='textContent').p.text.strip()
    imgs = soup.findAll('img', class_='bigImage')
    data['img'] = [i.get('src') for i in imgs]
    data['phone'] = get_phone(url)
    data['link'] = url
    return data


def to_html(in_file, out_file):
    with open(in_file, 'r') as f, open(out_file, 'w') as h:
        head = '''
            <!doctype html>
            <html>
            <head>
                <meta charset='utf-8'
            </head>
            <body>
            <table border='1'>
            '''
        r = csv.reader(f)
        rownum = 0
        h.write(head)
        for row in r:
            if rownum == 0:
                h.write('<tr>')
                for col in row:
                    h.write('<th>' + col + '</th>')
                h.write('</tr>')
            else:
                h.write('<tr>')
                for col in row:
                    h.write('<td>' + col + '</td>')
                h.write('</tr>')
            rownum += 1
        h.write('</table></body></html>')
