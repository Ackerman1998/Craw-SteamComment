#steam 评论，用户信息爬取 
import requests
import time
import xlwt
import urllib
import string
import bs4
import re
from bs4 import BeautifulSoup
appName = "PUBG"
appid = input("steam：请输入appid：")
maxDataSize = 10000
maxDataSize = input("请输入要请求数据的条数(10的倍数)：")
listAllContent = [] #所有的评论数据
nextCursor = "*" #索引下一页评论的cursor
reloadDataNum = 0 #重新拉取次数
reloadDataNumMax = 5 #重新拉取次数最大 = 5 ， 超过次数结束爬取。
lastedNum = 0
totalEndNum = 0
# PUBG 578080
def dict_encode_url(data: dict) -> str:
    return '&'.join(f"{urllib.parse.quote(i, encoding='utf-8')}={urllib.parse.quote(data[i], encoding='utf-8')}" for i in data)
# 获取游戏名字
def getGameName() :
    global appName
    resp = requests.get((f"https://store.steampowered.com/app/{appid}"),timeout=5)
    #print(resp.text)
    soup= BeautifulSoup(resp.text,"lxml")
    # Note=open('xxx.txt',mode='w', encoding='utf-8')
    # Note.write(soup.prettify()) 
    for business in soup.find_all('span',{'itemprop': ['name']}):
        print("获取游戏名字:")
        appName = business.string
        appName = appName.replace(":","-")  
        appName = appName.replace(":","-")  
        appName = appName.replace("/","-")  
        appName = appName.replace("|","-")  
        appName = appName.replace("?","-")  
        appName = appName.replace("？","-")  
        appName = appName.replace(">","-")  
        appName = appName.replace("<","-")  
        print(appName)
    time.sleep(1)
def getInitCursorValue() :
    isEnd = False
    global reloadDataNum
    global nextCursor
    global lastedNum
    global totalEndNum
    headers = {
    'Content-Type': 'application/json'
    }
    try:
        resp = requests.get((f"https://store.steampowered.com/appreviews/{appid}?cursor={nextCursor}&language=schinese&day_range=365&review_type=all&purchase_type=all&filter=recent"),timeout=5).json()
    except Exception as e:
        print(f"request failed：请求评论失败，尝试重新拉取...{reloadDataNum}")
        resp = ""
        isEnd = True
        reloadDataNum = reloadDataNum + 1
        time.sleep(1)
    if isEnd :
        return isEnd
    reloadDataNum = 0 #reset
    print(f"request completed , data list len ={len(listAllContent)}")
    if lastedNum == len(listAllContent):
        totalEndNum = totalEndNum + 1
        print(f"request failed：请求不到更多评论...{totalEndNum}")
        if totalEndNum >= reloadDataNumMax :
            print(f"结束请求...")
            isEnd = True
            reloadDataNum = 5
            time.sleep(1)
            return isEnd
    else:
        lastedNum = len(listAllContent)
        totalEndNum = 0 
    cursor =  resp["cursor"] 
    cursor = cursor.replace("+","%2B")     
    nextCursor = cursor
    html = resp["html"] #本页评论数据
    soup= BeautifulSoup(html,"lxml")
    #解析 用户名
    listName = []
    listRecommend = []
    listTime = []
    listComment = []
    for business in soup.find_all('div', class_="persona_name"):
        for bb in business.find_all('a') :
            listName.append(bb.string)
    #解析 是否推荐
    for business in soup.find_all('div', class_="title ellipsis"):
        listRecommend.append(business.string)
    #解析 游戏时长
    for business in soup.find_all('div', class_="hours ellipsis"):
        text1 =  business.text.replace("\r\n\t\t\t\t\t\t","")     
        text2 =  text1.replace("\t\t\t\t\t\t\t\t\t\t\t","")    
        listTime.append(text2)
    #解析 游戏评论
    for business in soup.find_all('div', class_="content"):
        text1 =  business.text.replace("\r\n\t\t\t\t\t","")     
        text2 =  text1.replace("\t\t\t\t\t\n","")     
        listComment.append(text2)
    # all data
    for number in range(0,len(listComment)) :
        list1 = []
        list1.append(listName[number])
        list1.append(listRecommend[number])
        list1.append(listTime[number])
        list1.append(listComment[number])
        listAllContent.append(list1)
    return isEnd
def fun2(lis) :          #保存数据
    print("开始存储!")
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  
    sheet = book.add_sheet("游戏数据", cell_overwrite_ok=True)  
    col = ["用户名","推荐",  "游戏时长",  "评论"]
    for i in range(0, 4):
        sheet.write(0, i, col[i])  # 列名
    for i in range(1, len(lis)+1):
        print('已经存储', i - 1, '行数据')
        for j in range(0, len(lis[i-1])):
            sheet.write(i, j, lis[i - 1][j])
    tt = f"游戏[{appName}][appid {appid}]评论数据[{maxDataSize}条].xls"
    print(tt)
    book.save(f"游戏[{appName}][appid {appid}]评论数据[{maxDataSize}条].xls")
if __name__ == '__main__':
    getGameName()
    while(len(listAllContent)<(int)(maxDataSize)):
        checkExit = getInitCursorValue()
        time.sleep(0.5)
        if checkExit == True :
            if reloadDataNum >= 5 :
                print("连接超时 5 次，结束")
                break
    fun2(listAllContent)
    time.sleep(1)