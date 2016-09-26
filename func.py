#!/usr/bin/python3
# coding: utf-8
# from bs4 import BeautifulSoup
import re
import requests


def get_phone(url):
    ''' get phone number from given link '''
    uid = re.findall(r'-ID(.*?).html', url)[0]
    r = requests.get('http://olx.ua/ajax/misc/contact/phone/' + uid)
    phones = re.findall(r'([ 0-9]+)', r.text)
    return [s for s in phones if s != ' ']


print(get_phone('http://www.olx.ua/obyavlenie/amortizatory-izh-planeta-yupiter-ID6P5lH.html#e50e5c6917;promoted'))
print(get_phone('www.olx.ua/obyavlenie/usilitel-na-tda7294-2-x-150-vt-mostovoy-IDlRCzg.html'))
