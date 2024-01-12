from app_store_scraper import AppStore
import string
import csv
from pprint import pprint
area = 'jp'
area = input("请输入地区名：")
appName = 'genshin'
appName = input("请输入游戏名：")
appid = '1517783697'
appid = input("请输入appid：")
maxDataSize = 10000
maxDataSize = input("请输入要请求数据的条数：")
minecraft = AppStore(country=area, app_name=appName,app_id = int(appid))
minecraft.review(how_many=int(maxDataSize))

# pprint(minecraft.reviews)
#pprint(minecraft.reviews_count)

data_list = []
#print(result)
for data in minecraft.reviews:
    name = data.get('userName')
    review = data.get('review')
    rating = data.get('rating')
    date = data.get('date')
    data_dict = {}
    data_dict['name'] = name
    data_dict['review'] = review
    data_dict['rating'] = rating
    data_dict['date'] = date
    data_list.append(data_dict)

appName = appName.replace(":","-")  
appName = appName.replace(":","-")  
appName = appName.replace("/","-")  
appName = appName.replace("|","-")  
appName = appName.replace("?","-")  
appName = appName.replace("？","-")  
appName = appName.replace(">","-")  
appName = appName.replace("<","-") 

with open(f'{area}-{appName}-{appid}.csv', 'w', encoding='utf-8-sig', newline='') as f:
    # 表头
    title = data_list[0].keys()
    # 创建writer
    writer = csv.DictWriter(f, title)
    # 写入表头
    writer.writeheader()
    # 批量写入数据
    writer.writerows(data_list)
print('csv文件写入完成')
xx = input("ok")