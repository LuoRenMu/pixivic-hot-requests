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
import sys
import os
sum = 1

downloadException = 0

#pixivic网站地址(防盗链)
pixivic_url = "https://pixivic.com/"
#pixivic排行请求地址
pixivic_imgJsonUrl="https://api.bbmang.me/ranks"
#pixivic伪链接
pixivic_imgFalseUrl="https://i.pximg.net"
#pixivic真链接
pixivic_imgTrueUrl="https://o.acgpic.net"


all_told = 50 #图片下载量

date_three = datetime.datetime.today() - datetime.timedelta(4)

date = date_three.strftime("%Y-%m-%d")

print(date)

print("CreateFileTime : 2021/9/5 10:36\nAuthor : YFen4nt0ren\nSoftware : PyCharm")

img_url=r"https://acgpic.net/" #正确的图片访问链接

file_download="D:\\images\\" #图片下载位置

#代理ip地址
proxies= {
    "https":"https://",
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 Edg/103.0.1264.62",
    "referer": pixivic_url,
    "origin": pixivic_url
}

if not os.path.exists(file_download):  # 是否存在这个文件夹
    print("未发现D盘存在文件images 正在创建文件夹")
    os.makedirs(file_download)  # 如果没有这个文件夹，那就创建一个

#循环爬取20页
for j in range(1,999):
    params = {
        "date": date,
        "page": j,
        "mode": "day",
        "pageSize": "30"
    }
    # 爬取一页内容 共25
    for i in range(0,22):
        if all_told is sum:
            print("已完成全部下载")
            SystemExit
        #获取下载链接位置if
        try:
            # xml url
            resp = requests.get(url=pixivic_imgJsonUrl, headers=headers, params=params)
            resp.encoding = 'utf-8'
            #print(resp.json()["message"])
            if resp.json()["message"] == "请求过于频繁":
                print(resp.json(),"当前ip已被暂时封禁 请稍后再试 5秒后程序结束")
                time.sleep(5)
                sys.exit()
            else:
                print(f"开始下载第{j}页")
                imgsrc=resp.json()["data"][i]["imageUrls"][0]["original"]
               # print(imgsrc)
                imgid = resp.json()["data"][i]["id"]
               # print(imgid)
                if os.path.isfile(f"{file_download}{imgid}.jpg"):
                    print(f"第{j}页 第{i}张图片{file_download}{imgid}.jpg 已存在")
                    continue
                else:
                #对反爬虫进行处理
                    imgsrc_split=re.findall(f"{pixivic_imgFalseUrl}(.*)",imgsrc)
                    img_download_url=f"{pixivic_imgTrueUrl}{imgsrc_split[0]}"
                #output url
                    #print(img_download_url)
                #img url
                    resp_img=requests.get(url=img_download_url,headers=headers)

                #download
                    with open(f"{file_download}{imgid}.jpg","wb") as f:
                        print(f"图片ID{imgid}数据已获取,开始下载")
                        f.write(resp_img.content)
                        print(f"#已成功下载第{sum}张图片{file_download}{imgid}.jpg ")
                        sum=sum+1
        except Exception:
            print(f"图片下载发生错误:{imgid}")
            print("数据代码:",resp.status_code,")
            if downloadException == 3 :
                print("无法处理异常(大概率ip被暂时封禁)")
                time.sleep(5)
                sys.exit()
print("全部完成")
resp.close()
