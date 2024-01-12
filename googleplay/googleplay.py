from google_play_scraper import Sort, reviews
import string
import csv
appid = 'com.fantome.penguinisle'
appid = input("请输入包名：")
maxDataSize = 10000
maxDataSize = input("请输入要请求数据的条数：")
result, continuation_token = reviews(
    appid,
    lang='en', # defaults to 'en'
    country='us', # defaults to 'us'
    sort=Sort.NEWEST, # defaults to Sort.NEWEST
    count=int(maxDataSize), # defaults to 100
    #filter_score_with=5 # defaults to None(means all score)
)

# If you pass `continuation_token` as an argument to the reviews function at this point,
# it will crawl the items after 3 review items.

result, _ = reviews(
    appid,
    continuation_token=continuation_token # defaults to None(load from the beginning)
)
data_list = []
#print(result)
for data in result:
    name = data.get('userName')
    content = data.get('content')
    score = data.get('score')
    at = data.get('at')
    appversion = data.get('appVersion')
    data_dict = {}
    data_dict['name'] = name
    data_dict['content'] = content
    data_dict['score'] = score
    data_dict['at'] = at
    data_dict['appversion'] = appversion
    data_list.append(data_dict)

with open(f'{appid}.csv', 'w', encoding='utf-8-sig', newline='') as f:
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
#f = open('data.txt', 'w')
# str1 = "".join(result)
# f.write(str1)
# # 关闭文件
# f.close()