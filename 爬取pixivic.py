# -*- codeing = utf-8 -*-
# @Time : 2021/9/5 10:36
# @Author : YFen4nt0ren
# @File : 爬取pixivic.py
# @Software : PyCharm
import requests
import datetime
import re
sum = 0
date_three = datetime.datetime.today() - datetime.timedelta(days=3)
date = date_three.strftime("%Y-%m-%d")
print(date)

img_url=r"https://acgpic.net/" #正确的图片访问链接
file_download="D:\\images\\" #图片下载位置
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
    "referer": "https://pixivic.com/"
}
#循环爬取20页
for j in range(1,20):
    print(f"开始下载第{j}页")
    params = {
        "date": date,
        "page": j,
        "mode": "day",
        "pageSize": "30"
    }
    #请求js数据渲染链接
    resp = requests.get(url="https://pix.ipv4.host/ranks", headers=headers, params=params)
    resp.encoding = 'utf-8'
    # 爬取一页内容 共25
    for i in range(0,25):
        #获取下载链接位置
        try:
            imgsrc=resp.json()["data"][i]["imageUrls"][0]["original"]
            imgid = resp.json()["data"][i]["id"]
            #对反爬虫进行处理
            imgsrc_split=re.findall("https://i.pximg.net(.*)",imgsrc)
            img_download_url=f"https://o.acgpic.net{imgsrc_split[0]}"
            #打印图片正确链接,因防盗链原因正常情况无法打开
            #print(img_download_url)
            #请求图片链接
            resp_img=requests.get(url=img_download_url,headers=headers)
            #下载图片
            with open(f"{file_download}{imgid}.jpg","wb") as f:
                f.write(resp_img.content)
            sum = sum+1
            print(f"第{j}页{i}下载完成 共完成{sum}")
            time.sleep(2)
        except Exception:
            print("错误下载")
print("全部完成")
resp.close()
