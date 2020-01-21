#-*-coding:utf-8-*-
# Arthur: Li Dong

import os
import sys
# include the path of ProxyList.py into sys.path
# so that the self-written module can be imported
sys.path.append("# path of ProxyList.py #")
from ProxyList import SocksProxyList
import time
import json
import queue
import threading
from urllib import request
from urllib import parse
from lxml import etree

header = {"User-Agent": "xxx"}
QueryList = ["xx"]
PathNameList = ["D:\\GoogleSpiderImage"]

CrawlQueue = queue.Queue()
ParseQueue = queue.Queue()
CrawlExit = False
ParseExit = False

class CrawlThread(threading.Thread):
    def __init__(self, ThreadName, CrawlQueue, ParseQueue, query):
        super(CrawlThread, self).__init__()
        self.ThreadName = ThreadName
        self.CrawlQueue = CrawlQueue
        self.ParseQueue = ParseQueue
        self.query = query
    def run(self):
        print(self.ThreadName + " starts")
        while not CrawlExit:
            try:
                full_url = "https://www.google.com/search?q=" + self.query + "&source=lnms&tbm=isch"
                ijn = self.CrawlQueue.get(block=False)
                img_start = ijn * 100
                rqo_main = request.Request(full_url, headers=header)
                rp_main = request.urlopen(rqo_main).read().decode("utf-8")
                # look for the "ei" value in the HTML document
                htmldom_main = etree.HTML(rp_main)
                str_contain_ei = htmldom_main.xpath("//script/text()")[0]
                ei_value = str_contain_ei[(str_contain_ei.find("{kEI:\'") + len("{kEI:\'")): str_contain_ei.find("\',",str_contain_ei.find("kscs:\'") + len("{kEI:\'") + 1)]
                # look for the data-ved value in the HTML document
                ved_value = htmldom_main.xpath("//div[@id=\"rg\"]/@data-ved")[0]
                # Generate the urls of the lists of images
                img_list_url = "https://www.google.com/search?ei=" + ei_value + "&q=" + self.query + "&tbm=isch&ved=" + ved_value + "&ijn=" + str(ijn) + "&start=" + str(img_start) + "&asearch=ichunk&async=_id:rg_s,_pms:s,_jsfs:Ffpdje,_fmt:pc"
                print(img_list_url)
                rqo_img_list = request.Request(img_list_url, headers=header)
                rp_img_list = request.urlopen(rqo_img_list).read().decode("utf-8")
                htmldom_img_list = etree.HTML(rp_img_list)
                img_info_data_ri = htmldom_img_list.xpath("//div[@jscontroller]/@data-ri")
                img_info_url = htmldom_img_list.xpath("//div[@class=\"rg_meta notranslate\"]/text()")
                for num in range(len(img_info_url)):
                    dict_img_info = json.loads(img_info_url[num])
                    img_url = dict_img_info["tu"]
                    rqo_img = request.Request(img_url, headers=header)
                    rp_img = request.urlopen(rqo_img)
                    self.ParseQueue.put((rp_img, img_info_data_ri[num]))
            except queue.Empty:
                pass
        print(self.ThreadName + " ends")


class ParseThread(threading.Thread):
    def __init__(self, ThreadName, ParseQueue, query, PathName):
        super(ParseThread, self).__init__()
        self.ThreadName = ThreadName
        self.ParseQueue = ParseQueue
        self.query = query
        self.PathName = PathName
    def run(self):
        print(self.ThreadName + " starts")
        while not ParseExit:
            try:
                tuple_rp_img = self.ParseQueue.get(block=False)
                if os.path.exists(self.PathName + "\\" + self.query) == False:
                    os.mkdir(self.PathName+ "\\" + self.query)
                filename = self.PathName + "\\" + self.query + "\\" + tuple_rp_img[1] + ".png"
                with open(filename, "ab") as f:
                    f.write(tuple_rp_img[0].read())
            except queue.Empty:
                pass
        print(self.ThreadName + " ends")


def GoogleImageDownloader(query, NumberWanted):
    """
    Search for and download images from Google
    :param query (str): Keyword of which images you want to search for
    :param NumberWanted (int): Number of images that you want to download
    :return: None
    """
    start_time = time.time()
    print("starting-time:", time.ctime())
    # generate the proxy handler
    proxy_handler = request.ProxyHandler({SocksProxyList[2][0]: SocksProxyList[2][1]})
    opener = request.build_opener(proxy_handler)
    request.install_opener(opener)
    quoted_query = parse.quote(query)
    # fill the CrawlQueue and ParseQueue
    ijn_uplimit = NumberWanted // 100
    global CrawlQueue
    CrawlQueue.__init__(ijn_uplimit+1)
    for num in range(ijn_uplimit+1):
        CrawlQueue.put(num)
    global ParseQueue
    ParseQueue.__init__(NumberWanted)
    # name of the threads
    CrawlNameList = ["CrawlThread1", "CrawlThread2", "CrawlThread3"]
    ParseNameList = ["ParseThread1", "ParseThread2", "ParseThread3"]
    CrawlThreadList = []
    ParseThreadList = []
    for ThreadName in CrawlNameList:
        crawl_thread = CrawlThread(ThreadName, CrawlQueue, ParseQueue, quoted_query)
        crawl_thread.start()
        CrawlThreadList.append(crawl_thread)
    for ThreadName in ParseNameList:
        parse_thread = ParseThread(ThreadName, ParseQueue, query, PathNameList[0])
        parse_thread.start()
        ParseThreadList.append(parse_thread)
    while not CrawlQueue.empty():
        pass
    global CrawlExit
    CrawlExit = True
    print("All CrawlThreads are finished")
    for item in CrawlThreadList:
        item.join()
    while not ParseQueue.empty():
        pass
    global ParseExit
    ParseExit = True
    for item in ParseThreadList:
        item.join()
    print("All ParseThreads are finished")
    ending_time = time.time()
    print("ending-time:", time.ctime())
    print("lasting time:", ending_time - start_time)


if __name__ == "__main__":
    for item in OueryList:
      GoogleImageDownloader(item, 999)
