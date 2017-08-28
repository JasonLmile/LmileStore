　以[顶点小说网][1]为例，试着爬取网站上的[武侠修真专题][2]的全部小说。

　　“不积跬步，无以至千里”。爬取全部小说先从一本小说开始，以小说《大泼猴》为例。首先，试着爬取小说中的一个章节：
```Python3
import re
from urllib import request
# Ｐython3自带的基本库

url = "http://www.x23us.com/html/51/51695/20781310.html"
# 要爬取的url

req = request.Request(url)
# 创建Request对象

response = request.urlopen(req)
# 打开对象

html = response.read().decode('gbk')
# 读取对象并用gbk解码
print(html)
```

　　在这个过程中，由于网站的编码格式为gbk，如果不用gbk格式解码，界面就会变成这样：
　　![这里写图片描述](http://img.blog.csdn.net/20170827215709247?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbHYxOTk4MDUyMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　而解码后则长这样：
　　![这里写图片描述](http://img.blog.csdn.net/20170827215736694?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbHYxOTk4MDUyMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
	
　　所以说以后抓取网站的时候要注意编码格式！！！
　　现在我们拿到网页的内容了，接下来的任务就是删选出文章内容了。首先我们打开浏览器查看元素:
　　![这里写图片描述](http://img.blog.csdn.net/20170825230811293?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbHYxOTk4MDUyMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　![这里写图片描述](http://img.blog.csdn.net/20170825231001149?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbHYxOTk4MDUyMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　结合之前打印的源代码内容，发现所有内容都出现在“<ｄｄ id="contents">”与“/ｄｄ>”之间，所以可以根据这个来制定匹配的模板：
　```
　pattern = re.compile(<dd id="contents">(.*?)/<dd>)
　```
　之后再把一些不必要的内容替换掉，爬取一章的任务就完成了：
```Python3
import re
from urllib import request
#Python3自带的标准库

url = "http://www.x23us.com/html/51/51695/20781310.html"
# 要爬取的url

req = request.Request(url)
# 创建Request对象

response = request.urlopen(req)
# 打开对象

html = response.read().decode('gbk')
# 读取对象并用gbk解码

pattern = re.compile(r'<dd id="contents">(.*?)</dd>)# 匹配内容的格式

content = re.findall(pattern,html)[0]
# 找出匹配的内容,findall输出的为一个列表

content = content.replace("&nbsp;&nbsp;&nbsp;&nbsp;","\n    ").replace('<br />','')
# 替换掉不需要的内容

print(content)
```
　　将它稍微整理一下，得到以下代码，它的功能是输入小说章节的地址，打印出章节内容：
```Python3
import re
from urllib import request


def getHtml(url):
    """输入url得到网页界面"""
    req = request.Request(url)
    # 创建Request对象

    response = request.urlopen(req)
    # 打开对象

    html = response.read().decode('gbk')
    # 读取对象并用gbk解码

    return html

def selectContent(html):
    """输入网页获得小说章节内容"""
    pattern = re.compile(r'<dd id="contents">(.*?)</dd>')
    # 匹配内容的格式

    content = re.findall(pattern,html)[0]
    # 找出匹配的内容,findall输出的为一个列表

    content = content.replace("&nbsp;&nbsp;&nbsp;&nbsp;","\n    ").replace('<br />','')
    # 替换掉不需要的内容

    return content

def getPage(url):
    """输入url打印章节内容"""
    html = getHtml(url)
    content = selectContent(html)
    print(content)

url = "http://www.x23us.com/html/51/51695/20781310.html"
# 要爬取的url

getPage(url)

```

　　接下来要做的是获取小说的章节地址，并依次输入getPage()函数中：
```Python3
import re
from urllib import request


def getHtml(url):
    """输入url得到网页界面"""
    req = request.Request(url)
    # 创建Request对象

    response = request.urlopen(req)
    # 打开对象

    html = response.read().decode('gbk')
    # 读取对象并用gbk解码

    return html

def selectContent(html):
    """输入网页获得小说章节内容"""
    pattern = re.compile(r'<dd id="contents">(.*?)</dd>')
    # 匹配内容的格式

    content = re.findall(pattern,html)[0]
    # 找出匹配的内容,findall输出的为一个列表

    content = content.replace("&nbsp;&nbsp;&nbsp;&nbsp;","\n    ").replace('<br />','')
    # 替换掉不需要的内容

    return content

def getPage(url):
    """输入url打印章节内容"""
    html = getHtml(url)
    content = selectContent(html)
    print(content)

book_url = "http://www.x23us.com/html/51/51695/"
# 书籍大泼猴的目录地址

book_html = getHtml(book_url)
# 获取书籍目录页面

catalog_pattern = re.compile(r'<td class="L"><a href="(.*?)">(.*?)</a></td>')
# 书籍章节链接及名称的匹配格式

catalog_list = re.findall(catalog_pattern,book_html)
# 列表中每个元素都是一个包含章节链接与名称的列表

for catalog in catalog_list:
    """循环获取章节链接，打印章节名称与内容"""

    catalog_url = book_url + catalog[0]
    # 获取真正的章节链接

    print(catalog[1])
    # 打印章节名称
    
    getPage(catalog_url)

    key = input("按q退出")
    if key == 'q':
        break

```
　　如图所示，这简单的实现了在线阅读的功能，只不过只能选择继续(按回车键)或退出(输入q再按回车)：
　　![这里写图片描述](http://img.blog.csdn.net/20170827215446100?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbHYxOTk4MDUyMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　将上面那段代码再封装一下，加上下载功能:
```Python3
import re
from urllib import request

class ddBookSpider:
    def __init__(self,url):
        """初始化书籍地址"""
        self.book_url = url
    
    def getHtml(self,url,times=3):
        """输入url得到网页界面，捕获到异常后再尝试3次"""
        try:
            req = request.Request(url)
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
                return getHtml(url,times-1)
        return html

    def selectContent(self,html):
        """输入网页获得小说章节内容"""
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

    def getCataloglist(self,book_html):
        """输入书目录的界面内容获得包含书的章节链接及名称的列表"""
        
        catalog_pattern = re.compile(r'<td class="L"><a href="(.*?)">(.*?)</a></td>')
        # 书籍章节链接及名称的匹配格式

        catalog_list = re.findall(catalog_pattern,book_html)
         # 列表中每个元素都是一个包含章节链接与名称的列表

        return catalog_list

    def getBook(self):
        """输入书籍链接下载书籍"""
        book_html = self.getHtml(self.book_url)
        catalog_list = self.getCataloglist(book_html)
        
	for catalog in catalog_list:
            """循环获取章节链接及名称"""

            catalog_url = self.book_url + catalog[0]
            # 获取真正的章节链接

            content =self.getPage(catalog_url)
            #得到章节内容
            
            title = catalog[1]
            #得到章节名称

            self.download(title,content)
            
            print("============%s下载完毕============"%title)
            # 提示下载过程

    def download(self,title,content):
        """下载章节"""
        f = open("~/Desktop/大泼猴.txt",'a+')
        # 打开文件
        
        f.write(title + '\n')
        f.write(content + '\n' + '\n')
        # 写入文件
        
        f.close()
        # 关闭文件


book_url = "http://www.x23us.com/html/51/51695/"
# 书籍大泼猴的目录地址

dapohouSpider = ddBookSpider(book_url)
dapohouSpider.getBook()
```
　　运行之后，稍等一会这本书就会下载到桌面上：
　　![这里写图片描述](http://img.blog.csdn.net/20170827215307302?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbHYxOTk4MDUyMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　　上面这个类实现了输入一本书的链接地址可下载书籍内容的功能，将它扩展一下，爬取一个专题的书籍地址，并将书籍下载下来。通过观察发现专题的url都是“http://www.x23us.com/class/2_1.html”的形式,而且第几页“_”后的数字就是几。可以通过这一点达到抓取整个专题书籍的目的：
```Python3
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
        f = open("~/Documents/Book/"+self.book_name+".txt",'a+')
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
# 武侠修真专题第一页的链接

xiuzhenSpider = ddBookSpider(topic_url)
xiuzhenSpider.getTopicbook()
```
　　运行之后，看着终端上闪出的提示还是蛮有成就感的呢!^_^
　　![这里写图片描述](http://img.blog.csdn.net/20170827214544073?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvbHYxOTk4MDUyMw==/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast)
　
-----------

[1]: http://www.x23us.com/
[2]:http://www.x23us.com/class/2_1.html