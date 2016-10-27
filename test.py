import requests
from bs4 import BeautifulSoup
import re

res = requests.get("https://tw.search.bid.yahoo.com/search/product;_ylt=AlVvPYF4uAi_N312wTXpbl1yFbN8;_ylv=3?p=iphone+6+plus+%E6%89%8B%E6%A9%9F%E6%AE%BC&property=auction&sub_property=auction&srch=product&aoffset=0&poffset=0&pg=1&pptf=3&act=srp&rescheck=1&pmt=30&its=16&cid=4638850&clv=4&sort=etime&nst=1&fr=aucpromo&show=pic&show_flag=1&view=pic&hpp=hp_topkeyword_04_07&fr=aucpromo")

soup = BeautifulSoup(res.text, 'lxml')

count = 1

for item in soup.select(' .srp-pdcontent'):
    print('======[',count,']=========')
    print(item.select(' .srp-pdtitle')[0].text.strip())
    print(item.select(' .srp-pdprice')[0].text.strip())
    count += 1