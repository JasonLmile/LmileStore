import requests
from bs4 import BeautifulSoup
import time

class WHavenSpider:
    """用于爬取WallHaven高清壁纸"""
    def __init__(self,topic_url):
        """初始化抓取的主题url"""
        self.topic_url = topic_url

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
        f = open("/home/lmile/Documents/DotaImg/"+name,'wb')
        
        f.write(pic_html)
        
        f.close

    def work(self):
        """工作方法"""
        topic_html = self.getHtml(self.topic_url)

        for url in self.getTopic(topic_html):
        
            html = self.getHtml(url)
            part_list = self.selectPartlist(html)

            for part in part_list:
               
                page_url = part['href']
                
                page_html = self.getHtml(page_url)

                img_url = self.selectImg(page_html)       
                
                name = img_url[-10:]

                img_html = self.getHtml(img_url)

                self.download(name,img_html)

                print("==========%s图片下载完毕=========="%name)
            print("==========第%s页下载完毕=========="%url.rpartition('=')[-1])

    def getTopic(self,topic_html):
        """输入专题页面得到专题所有页面的url,返回一个迭代器对象"""
        topic_soup = BeautifulSoup(topic_html,'lxml')
        
        num_generator = topic_soup.h2.strings
        # h2节点下的多个内容,为'generator'不能通过下标遍历
        
        num_list = list(num_generator)
        
        num = num_list[-1].split(' ')[-1]

        for i in range(1,int(num)):
            """循环迭代产生出url"""
            topic_url = self.topic_url + 'page=' + str(i)
            
            yield topic_url
    
url = "https://alpha.wallhaven.cc/search?q=dota2&search_image=&"
# dota2专题首页url

dotaspider = WHavenSpider(url)
dotaspider.work()
