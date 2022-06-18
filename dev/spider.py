# 这个模块就只负责网络和爬虫的任务


import requests
import re
import os

class spider:
    def __init__(self):
        
        self.headers = {    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 "}
        self.kw = {}
        self.link = "https://www.bilibili.com/"

    def get_Bilibili_Pictures(self):
        web_Page_Res = requests.get(self.link,params = self.kw, headers = self.headers)
        web_Page_html_text = str(web_Page_Res.text)
        match_iamge_Url_List = re.findall(r'srcset=.+?[.]webp',web_Page_html_text)
        image_Url_List = []
        for obj in match_iamge_Url_List:
            image_Url_List.append(obj[8:-18])        
        image_Count = len(image_Url_List)
        # os.makedirs("data")
        data_path = "data"
        for obj in image_Url_List:
            fileName = str(image_Url_List.index(obj))+".jpg"
            file_Path = os.path.join(data_path,fileName)
            with open(file_Path,"wb") as fp:
                if obj[0]=="h":
                    url_Link = obj
                else:
                    url_Link = "https:"+obj
                pic_Res = requests.get(url_Link, params = self.kw, headers = self.headers)
                fp.write(pic_Res.content)
                
                
if __name__ == "__main__":
    sp = spider()
    sp.get_Bilibili_Pictures()
