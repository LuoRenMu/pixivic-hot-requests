# -*- codeing = utf-8 -*-
# @Time : 2021/9/5 10:36
# @Author : YFen4nt0ren
# @File : 爬取pixivic.py
# @Software : PyCharm
from tkinter.tix import IMMEDIATE
import requests
import datetime
import time
import re
import os
sum = 1
date_three = datetime.datetime.today() - datetime.timedelta(days=4)
date = date_three.strftime("%Y-%m-%d")
print(date)
print("Time : 2021/9/5 10:36\nAuthor : YFen4nt0ren\nSoftware : PyCharm")
img_url=r"https://acgpic.net/" #正确的图片访问链接
file_download="D:\\images\\" #图片下载位置
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "referer": "https://pixivic.com/"
}
#循环爬取20页
for j in range(1,999):
    print(f"开始下载第{j}页")
    params = {
        "date": date,
        "page": j,
        "mode": "day",
        "pageSize": "30"
    }
    #xml url
    resp = requests.get(url="https://pix.ipv4.host/ranks", headers=headers, params=params)
    resp.encoding = 'utf-8'
    # 爬取一页内容 共25
    for i in range(0,22):
        #获取下载链接位置if
        try:
            imgsrc=resp.json()["data"][i]["imageUrls"][0]["original"]
            imgid = resp.json()["data"][i]["id"]
            if os.path.isfile(f"{file_download}{imgid}.jpg"):
                print(f"第{j}页 第{i}张图片{file_download}{imgid}.jpg 已存在")
                continue
            else:
            #对反爬虫进行处理
                imgsrc_split=re.findall("https://i.pximg.net(.*)",imgsrc)
                img_download_url=f"https://o.acgpic.net{imgsrc_split[0]}"
            #output url
               # print(img_download_url)
            #img url
                resp_img=requests.get(url=img_download_url,headers=headers)
            #download
                with open(f"{file_download}{imgid}.jpg","wb") as f:
                    f.write(resp_img.content)
                    print(f"#已成功下载第{sum}张图片{file_download}{imgid}.jpg ")
                    sum=sum+1
        except Exception:
            print(i,"错误")
print("全部完成")
resp.close()
