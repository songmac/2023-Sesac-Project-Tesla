#네이버뉴스 1개 크롤링

import requests
import pandas as pd
from bs4 import BeautifulSoup

def news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    
    media_element = soup.select_one('a.media_end_head_top_logo img')
    if media_element:
        media = media_element.get('title')
    else:
        media = None
    
    
    title_element = soup.select_one('h2#title_area')
    if title_element:
        title = title_element.text
    else:
        title = None
    

    date_element = soup.select_one('span.media_end_head_info_datestamp_time')
    if date_element:
        date = date_element.get('data-date-time')
    else:
        date = None
    
    
    content_element = soup.select_one('article#dic_area')
    if content_element:
        content = content_element.text.strip()
    else:
        content = None
    
    return {
        'title': title,
        'date': date,
        'media': media,
        'content': content,
        'url': url
    }
news('https://n.news.naver.com/mnews/article/001/0013674088?sid=104')



#네이버뉴스 페이지+원하는 날짜 크롤링

def news_list(keyword, startdate, enddate):
    li = []
    h = {'User-Agent': '...',  
         'Referer': '...',  
         'cookie': '...'}  

    for d in pd.date_range(startdate, enddate):
        str_d = d.strftime("%Y.%m.%d")
        page = 1
        print(str_d)
        while True:
            start = (page - 1) * 10 + 1
            print(page)
            URL = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query={0}&sort=2&photo=0&field=0&pd=3&ds={1}&de={2}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from{3}to{4},a:all&start={5}".format(keyword, str_d, str_d, str_d.replace(".", ""), str_d.replace(".", ""), start)

            res = requests.get(URL, headers=h)
            soup = BeautifulSoup(res.text, "html.parser")

            if soup.select_one(".api_noresult_wrap"):
                break

            news_list = soup.select("ul.list_news li")

            for item in news_list:
                if len(item.select("div.info_group a")) == 2:
                    li.append(news(item.select("div.info_group a")[1]['href']))
            page = page + 1

    return pd.DataFrame(li, columns=['title', 'date', 'media', 'content', 'url'])

result_df = news_list('테슬라', '2023.02.01', '2023.02.28')

result_df
result_df.to_csv('news_data3.csv', index=False, encoding='utf-8-sig')



#csv파일 저장위치

import os
current_directory = os.getcwd()
print("Current Directory:", current_directory)

#화이팅!