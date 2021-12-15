# from bs4 import BeautifulSoup
# import requests
#
# words = ['旗帜','计算机','首都','乾坤','理工']
# for word in words :
#     r=requests.get('https://hanyu.baidu.com/s?wd='+word+'&device=pc&from=zici')
#     r.encoding='utf-8'
#     soup = BeautifulSoup(r.text,'lxml')
#     print('{:-^60}'.format(word))
#     for p in soup.find(id='basicmean-wrapper').div.dd:
#         print(p.string.strip())




# coding:utf-8
import requests
from bs4 import BeautifulSoup

def spider(url,headers):
    with open('renming.txt', 'w', encoding='utf-8') as fp:
        r = requests.get(url,headers=headers)
        r.encoding = 'GB2312'
        # test=re.findall('<li>< a href= >(.*?)</ a></li>',r.text)
        # print(test)
        soup = BeautifulSoup(r.text, "html.parser")
        for news_list in soup.find_all(class_="list1"):
            content = news_list.text.strip()
            fp.write(content)
    fp.close()

if __name__=="__main__":
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/55.0.2883.87 Safari/537.36'}

    url = 'http://www.people.com.cn/'
    spider(url, headers)