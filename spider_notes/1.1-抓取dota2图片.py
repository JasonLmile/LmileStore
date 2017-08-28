import requests
from bs4 import BeautifulSoup
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}


url = "https://alpha.wallhaven.cc/search?q=dota2&search_image=&"
# dota2壁纸的网址

req = requests.get(url)
# 获取url网页

html = req.content
# 网页内容

soup = BeautifulSoup(html,'lxml')
# 对内容进行处理解析

a_list = soup.find('section',class_='thumb-listing-page').find("ul").find_all('a',class_='preview')
# 获得a标签的列表

for a in a_list:
    # print(a['href'])
    # 打印出每个高清图片所在的网址
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0','Referer':url}
    # 头部信息
    img_req = requests.get(a['href'],headers=headers)
    # 获取页面
    img_html = img_req.content
    # 获得页面内容
    img_soup = BeautifulSoup(img_html,'lxml')
    # 对页面进行处理
    img = img_soup.find('main').find('section',id='showcase').find("img")['src']
    # 找出高清图片网址
    true_img = 'https:' + img
    # 加上前缀
    # print(ture_img)

    pic_req = requests.get(true_img,headers=headers)

    pic_html = pic_req.content

    name = true_img[-10:]

    f = open(name,'ab')
    f.write(pic_html)
    f.close
    
    k = input('q结束:')
    if k =='q':
        break;
