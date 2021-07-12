#coding:utf-8
import requests
#coding:utf-8
import requests
import re
import time
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
f = open("picture.txt", "r", encoding="utf-8")  # 返回一个文件对象
line = f.readline()  # 调用文件的 readline()方
head = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

def getImg(url,name):
    pathName = "picture\ " + name + ".jpg"
    urllib.request.urlretrieve(url, pathName)


PhotoName = 1
while line and PhotoName:
    line = f.readline()
    lst = line.split(" ")
    print(lst[0])
    PhotoName += 1
    if len(lst) > 1:
        # time.sleep(2)
        name = lst[0]
        url = lst[1]
        try:
            getImg(url, name)
            print("You are downloading the %d photos" % PhotoName)
        except ValueError:
            print("")
f.close()
