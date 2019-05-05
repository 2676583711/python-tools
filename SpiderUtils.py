import requests
from lxml import etree

from tools import EmailUtils


class SpiderUtils():
    # 初始化
    def __init__(self, startUrl, topicXpath, textXpath, hrefXpath, fileName, index, nextHalfUrl):
        # 初始url
        self.startUrl = startUrl
        # 章节名的xpath
        self.topicXpath = topicXpath
        # 正文内容的xpath
        self.textXpath = textXpath
        # href的xpath
        self.hrefXpath = hrefXpath
        # 写入文件的路径加名字
        self.fileName = fileName
        # 下一页的href的索引
        self.index = index
        # 下一页的url的上半截
        self.nextHalfUrl = nextHalfUrl

    # 进行爬虫工作,根据url发起请求,返回html文本数据
    def spider(self, url):

        #   定义user - agent
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"}
        try:
            # 接收响应数据
            response = requests.get(url=url, headers=headers)
        # 处理发送请求可能出现的异常
        except:
            headers = {"User-Agent":
                           "Mozilla/5.0 (X11; Linux x86_64…) Gecko/20100101 Firefox/66.0"}
            # 如果出现异常很大可能是https请求，上面的是针对http协议的请求
            response = requests.get(url=url, headers=headers)
            response = requests.get(url=url, headers=headers)

        try:
            # 捕捉响应数据中获取文本并编码可能出现的异常
            try:
                # 从响应数据中，获取文本并编码
                html = response.content.decode("utf-8")
            except:
                html = response.content.decode("gbk")
        except:
            html = response.text

        # 使用xapth解析目标数据,并返回html文本数据
        return etree.HTML(html)

    # 爬去的结果写入硬盘文件
    def writeFile(self, fileName, topic, text):
        with open(fileName, "a")as f:
            # 写入章节名
            f.writelines("".join(topic))
            # 换行
            f.writelines("\n")
            # 写入正文
            f.writelines("".join(text))
            # 写入换行
            f.writelines("\n\n\n\n")
            # 关闭文件
            f.close()
            print("OK")

    # 解析html文本数据提取目标数据并写入硬盘文件,返回下一页的url的下半截
    def parse(self, xml):
        # 章节名称
        # title = xml.xpath("//div[@class='title']/h1/text()")
        global topic
        topic = xml.xpath(self.topicXpath)

        # 小说内容
        # text = xml.xpath("//div[@id='content']//text()")
        text = xml.xpath(self.textXpath)

        # 获取下一页的url数组
        # href = xml.xpath("//div[@class='jump']//@href")
        href = xml.xpath(self.hrefXpath)
        print(href)

        # 写入爬取的章节名和正文
        self.writeFile(self.fileName, topic, text)

        try:
            # 定义下一页的href
            # print("下一页:" + href[self.index])
            url = href[self.index]
            print(topic + "\t")

        # 如果出现异常,说明没有下一页了
        except:
            print("\n目前已经更新的小说已经爬取完毕了!!!")
            return None
        return url

    # 执行整个网站的爬取
    def execute(self):
        # 调用spider函数，返回html数据
        html = self.spider(self.startUrl)
        #  调用parse函数，返回下一页的url的下半截
        url = self.parse(html)
        while url != None:
            # 拼接下一页的url
            nextUrl = self.nextHalfUrl + url
            html = self.spider(nextUrl)
            url = self.parse(html)
            print(nextUrl + "\n")

        # 退出循环，表明文件写完了，此时可以发送附件了
        # filepath, sender, receiver, subject
        eu = EmailUtils(self.fileName, "liberalzhou@163.com", "liberalzhou@163.com", topic)
        eu.sendWithAtachment()


if __name__ == '__main__':
    startUrl = " http://www.biquge.li/220700/1131117.html"
    # //div[@id='content']//text()  xpath模板
    topicXpath = "//div[@class='bookname']/h1/text()"

    textXpath = "//div[@id='content']//text()"

    # //div[@class='key']//@href")
    hrefXpath = "//div[@class='bottem2']//@href"

    fileName = "/home/zhou/美漫世界的武者.txt"
    index = 2
    nextHalfUrl = "http://www.biquge.li/220700/"

    su = SpiderUtils(startUrl, topicXpath, textXpath,
                     hrefXpath, fileName, index, nextHalfUrl)
    su.execute()
