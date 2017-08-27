import re
from urllib import request

class ddBookSpider:

    def __init__(self,topic_url):
        """初始化书籍地址,注意topic_url必须为专题第一页的url"""
        self.book_url = ""
        self.book_name = None
        self.topic_url = topic_url
    def getHtml(self,url,times=4):
        """输入url得到网页界面"""
        try:
            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"}
            req = request.Request(url,headers=headers)
            # 创建Request对象

            response = request.urlopen(req)
            # 打开对象

            html = response.read().decode('gbk')
            # 读取对象并用gbk解码
        except Exception as a:
            print("出现%s错误,剩余次数:%d"%(a,times))
            if times<=0:
                print("重试失败")
                return ''
            else:
                return self.getHtml(url,times-1)
        return html

    def selectContent(self,html):
        """输入章节界面删选获得小说章节内容"""
        pattern = re.compile(r'<dd id="contents">(.*?)</dd>')
        # 匹配内容的格式

        content = re.findall(pattern,html)[0]
        # 找出匹配的内容,findall输出的为一个列表

        content = content.replace("&nbsp;&nbsp;&nbsp;&nbsp;","\n    ").replace('<br />','')
        # 替换掉不需要的内容

        return content

    def getPage(self,url):
        """爬取地址为url的章节内容"""
        html = self.getHtml(url)
        
        content = self.selectContent(html)
        
        return content


    def selectCataloglist(self,book_html):
        """输入书目录的页面获得包含书的章节链接及名称的列表"""

        catalog_pattern = re.compile(r'<td class="L"><a href="(.*?)">(.*?)</a></td>')
        # 书籍章节链接及名称的匹配格式

        catalog_list = re.findall(catalog_pattern,book_html)
         # 列表中每个元素都是一个包含章节链接与名称的列表

        return catalog_list

    def download(self,title,content):
        """下载章节"""
        f = open("/home/lmile/Documents/Book/"+self.book_name+".txt",'a+')
        # 打开文件
        
        f.write(title + '\n')
        f.write(content + '\n' + '\n')
        # 写入文件
        
        f.close()
        # 关闭文件

    def getBook(self):
        """输入书籍链接下载书籍"""
        book_html = self.getHtml(self.book_url)
        catalog_list = self.selectCataloglist(book_html)
        
        for catalog in catalog_list:
            """循环获取章节链接及名称"""

            catalog_url = self.book_url + catalog[0]
            # 获取真正的章节链接

            content =self.getPage(catalog_url)
            #得到章节内容
            
            title = catalog[1]
            #得到章节名称

            self.download(title,content)
            
            print("==========%s下载完毕=========="%title)
            # 提示下载完毕

    def selectBook(self,topic_html):
        """输入专题界面删选出书籍目录链接及名称"""

        book_pattern = re.compile(r']</a><a href="(.*?)" target="_blank">(.*?)</a></td>')
        # 书籍目录链接及书籍名称的匹配格式

        book_list = re.findall(book_pattern,topic_html)

        return book_list
    
    def getPagebook(self,topic_url):
        """输入专题某一页的链接下载这页下的书籍""" 
        topic_html = self.getHtml(topic_url)
        book_list = self.selectBook(topic_html)

        for book in book_list:
            """遍历下载每一本书"""
            self.book_url = book[0]
            self.book_name = book[1]
            
            print("==========%s下载开始=========="%self.book_name)
            self.getBook()
            print("==========%s下载完毕=========="%self.book_name)
            
    def getTopicbook(self):
        """输入一个专题第一页链接下载所有专题书籍"""
        page_html = self.getHtml(self.topic_url)
        page_pattern = re.compile(r'<em id="pagestats">1/(.*?)</em>')
        page_num = re.findall(page_pattern,page_html)[0]

        for i in range(1,int(page_num)-1):
            
            page_url = topic_url.replace('1',str(i))
            self.getPagebook(page_url)
            

topic_url = 'http://www.x23us.com/class/2_1.html'
# 仙侠专题第一页的链接

xianxiaSpider = ddBookSpider(topic_url)
xianxiaSpider.getTopicbook()
