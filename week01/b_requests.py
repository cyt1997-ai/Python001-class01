import requests
from lxml import etree

header = {
'Cookie': '__mta=46061339.1593251464007.1593259262114.1593260954217.10; uuid_n_v=v1; uuid=B664DE60B85B11EA974289B279A7041D90869F5A226647E78CFF03679CFFC146; _csrf=285e7aef20a798f88df66e73d311fd42962e46a56eb82b92dca16970c4dd2007; mojo-uuid=332e8f236f85eb79975793897a8190cc; _lxsdk_cuid=172f53002fdc8-0109b5500d17d3-f7d1d38-144000-172f53002fdc8; _lxsdk=B664DE60B85B11EA974289B279A7041D90869F5A226647E78CFF03679CFFC146; mojo-session-id={"id":"e735516561f96cc24c32a25fbb5bdfc4","time":1593267738759}; mojo-trace-id=1; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593252827,1593252854,1593255142,1593267739; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593267739; __mta=46061339.1593251464007.1593260954217.1593267739413.11; _lxsdk_s=172f62854d8-86e-4a1-79c%7C%7C3',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}

d_url ="https://maoyan.com"
p = '/films?showType=3'
url = d_url + p

my_list = []
my_list.append(('名称','类型','上映时间'))

#requests请求
def NeiRong(url):
    response = requests.get(url, headers=header)
 #   print(response.text)
    tree = etree.HTML(response.text)
    return tree

#解析主页面

link = NeiRong(url).xpath('//*[@class="channel-detail movie-item-title"]/a')

for i in range(0,10):  #取前10个电影信息
    #获取详情页地址
    page_url = d_url+link[i].attrib['href']

    print(page_url)
    #获取详情页内容
    page_tree = NeiRong(page_url).xpath('//*[@class="movie-brief-container"]')

    # 名称
    name_page = page_tree[0].xpath('h1')[0].text

    # 类型
    type_tree = page_tree[0].xpath('ul/li[1]/a')
    # 遍历 a 标签内容
    tpye_page = ''
    for i in type_tree:
        tpye_page = i.text

    # 时间
    time_page = page_tree[0].xpath('ul/li[3]')[0].text

    my_list.append((name_page,tpye_page,time_page))
import pandas

movie_xpath = pandas.DataFrame(data=my_list)

# windows需要使用gbk字符集
movie_xpath.to_csv('./movie_xpath.csv', encoding='gbk', index=False, header=False)





