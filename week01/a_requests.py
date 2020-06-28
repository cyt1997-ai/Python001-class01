import requests
from bs4 import BeautifulSoup as bs
import pandas

url = "https://maoyan.com/films"

querystring = {"showType":"3"}

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'host': "maoyan.com",
    'referer': "https://u.geekbang.org/lesson/18?article=252019",
    'sec-fetch-dest': "document",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "cross-site",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    }

response = requests.request("GET", url, headers=headers, params=querystring)


bs_info = bs(response.text, 'html.parser')
# print(response.text)



# 获取电影名称，和链接地址

mylist =[]
n = 0
mylist.append(('名称','类型','上映时间'))
for tags in bs_info.find_all('div', attrs={'class': 'movie-hover-info'}):
    n += 1
    if n <= 10 :

    #电影名称
        name = tags.find_all('div', attrs={'class': 'movie-hover-title'})[0].text.strip()
        name = name.split()[0]

    #类型
        leixing = tags.find_all('div', attrs={'class': 'movie-hover-title'})[1].text[4:].strip()

    #上映时间
        s_time = tags.find_all('div', attrs={'class': 'movie-hover-title'})[3].text[6:].strip()

        mylist.append((name,leixing,s_time))


movie1 = pandas.DataFrame(data=mylist)

# windows需要使用gbk字符集
movie1.to_csv('./movie1.csv', encoding='gbk', index=False, header=False)



