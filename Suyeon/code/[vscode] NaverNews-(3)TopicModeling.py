#네이버뉴스 1개 크롤링
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re, unicodedata
from string import whitespace


def news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    media_element = soup.select_one('a.media_end_head_top_logo img')
    media = media_element.get('title') if media_element else None
    title_element = soup.select_one('h2#title_area')
    title = title_element.text if title_element else None
    date_element = soup.select_one('span.media_end_head_info_datestamp_time')
    date = date_element.get('data-date-time') if date_element else None
    content_element = soup.select_one('article#dic_area')
    content = content_element.text.strip() if content_element else None
    return {
        'title': title,
        'date': date,
        'media': media,
        'content': content,
        'url': url
    }


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


def clean_byline(text):
    # 바이라인
    pattern_email = re.compile(r'[-_0-9a-z]+@[-_0-9a-z]+(?:\.[0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_url = re.compile(r'(?:https?:\/\/)?[-_0-9a-z]+(?:\.[-_0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_others = re.compile(r'\.([^\.]*(?:기자|특파원|교수|작가|대표|논설|고문|주필|부문장|팀장|장관|원장|연구원|이사장|위원|실장|차장|부장|에세이|화백|사설|소장|단장|과장|기획자|큐레이터|저작권|평론가|©|©|ⓒ|\@|\/|=|▶|무단|전재|재배포|금지|\[|\]|\(\))[^\.]*)$')
    result = pattern_email.sub('', text)
    result = pattern_url.sub('', result)
    result = pattern_others.sub('.', result)

    # 본문 시작 전 꺽쇠로 쌓인 바이라인 제거
    pattern_bracket = re.compile(r'^((?:\[.+\])|(?:【.+】)|(?:<.+>)|(?:◆.+◆)\s)')
    result = pattern_bracket.sub('', result).strip()

    return result



# 크롤링할 데이터 (키워드, 시작날짜, 종료날짜)
result_df = news_list('테슬라', '2022.05.01', '2022.05.31')
print(result_df)

# 크롤링 데이터, 데이터 프레임에 저장 및 필요없는 column 삭제
df = pd.DataFrame(result_df)
df.drop(['media', 'url'], axis=1, inplace = True)
df['content'] = df['content'].fillna('').astype(str).map(clean_byline)

# 유니코드 문자 전처리 및 정규 표현식 사용
pattern_whitespace = re.compile(f'[{whitespace}]+')
df['content'] = df['content'].str.replace(pattern_whitespace, ' ').map(lambda x: unicodedata.normalize('NFC', x)).str.strip()


# 전처리한 데이터 csv 파일로 저장
df['content'].to_csv('[2022-May]news_data_content.csv', index=False, encoding='utf-8-sig')