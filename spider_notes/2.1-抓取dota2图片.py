import requests
from bs4 import BeautifulSoup
import time

class WHavenSpider:
    """用于爬取WallHaven高清壁纸"""
    def __init__(self):
        pass

    def getHtml(self,url):
        """输入url输出页面内容"""
        req = requests.get(url)
        # 获取url网页

        html = req.content
        # 网页内容
        
        return html

    def selectPartlist(self,html):
        """输入页面删选出包含url部分的列表"""
        soup = BeautifulSoup(html,'lxml')

        part_list = soup.find('section',class_='thumb-listing-page').find("ul").find_all('a',class_='preview')

        return part_list

    def selectImg(self,img_html):
        """输入页面删选出图片url"""
        img_soup = BeautifulSoup(img_html,'lxml')
        # 对页面进行处理
        
        img = img_soup.find('main').find('section',id='showcase').find("img")['src']
        # 找出高清图片网址
        
        img_url = 'https:' + img
        # 加上前缀
        
        return img_url

    def download(self,name,pic_html):
        """下载图片"""
        f = open(name,'wb')
        
        f.write(pic_html)
        
        f.close

    def work(self,url):
        """工作方法"""
        html = self.getHtml(url)
        part_list = self.selectPartlist(html)

        for part in part_list:
           
            page_url = part['href']
            
            page_html = self.getHtml(page_url)

            img_url = self.selectImg(page_html)       
            
            name = img_url[-10:]

            img_html = self.getHtml(img_url)

            self.download(name,img_html)

url = "https://alpha.wallhaven.cc/search?q=dota2&search_image=&"

dotaspider = WHavenSpider()
dotaspider.work(url)


