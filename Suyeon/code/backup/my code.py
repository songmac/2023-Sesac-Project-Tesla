import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_news(URL) :
  res = requests.get(URL)
  soup = BeautifulSoup(res.text, "html.parser")

  if soup.select_one("h2#title_area span") != None:
    title = soup.select_one("h2#title_area span").text #제목
    date = soup.select_one("span.media_end_head_info_datestamp_time")['data-date-time'] #기사작성일시
    media = soup.select_one("a.media_end_head_top_logo img")['title'] #매체명 (예.한국경제)
    content = soup.select_one("div#newsct_article").text.replace("\n","") #기사원문

  else :
    return None

  return (title, date, media, content, URL)

# get_news("https://n.news.naver.com/mnews/article/014/0005075348?sid=101")

def get_news_list(keyword, startdate, enddate):
    li = []
    h = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36', 'Referer' : 'https://search.naver.com/search.naver?where=news&query=%ED%85%8C%EC%8A%AC%EB%9D%BC&sm=tab_opt&sort=2&photo=0&field=0&pd=0&ds=&de=&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Aall&is_sug_officeid=0&office_category=0&service_area=0', 'cookie':'NNB=KXDWSALR5HLWE; ASID=afc28e77000001821bee653700000062; _ga=GA1.2.852833469.1658355403; _ga_7VKFYR6RV1=GS1.1.1663030713.12.1.1663030726.47.0.0; NFS=2; m_loc=8e6c6458de8107ce6b301a2fdcaac47c270f10d32641f9fdfed1b5b1faac3e2c; NV_WETR_LAST_ACCESS_RGN_M="MDIxMzU1NTA="; NV_WETR_LOCATION_RGN_M="MDIxMzU1NTA="; recent_card_list=2936,3397,2717,3977; nx_ssl=2; nid_inf=-1453188587; NID_AUT=3O547E30xwR+LSPJWBh1H0BeJZ8z7w5GcYoFiB1oouz7XPFXgUYyapi0YaIPu/ed; NID_JKL=G/s4QbAdJVVTz69y/dBkR/9g00VQhbM8nxg71ZvVgyE=; NID_SES=AAABoKkgglCWz6aloghoOZ3uiyN2Gx8Ya6M3siOaeQCtWMn7TXgrPkganW/YVI931ONSrWmpB6IIM3p/mCMfueM9ekkTAuzM2mj8PfOoUbrV7BrzerfHGStcNmmb0QkiSuOy8AH1MwneQ7sJCTZBpPEfIbn9HUQ6S62sMy5oLJ0xqXedXxwQ4TsBa4+6Z6FWpVTIfmTzWMFt/M4pfpxYEbYAVBsfhLIsNPCjHLCrkoDdQPeUS949dDM9Xf8zpucBTRJrB6GwKaQDSeVWs+OgXngp1iusiktNnHZ7hEWDO5gyZCXkA7jV9njHKBDw6b58JD2La4eTPDBjq6xzUHaCAt+L7rGlpQ5FWHh1UF8XcyHGLdi2zQRHHSs9giWGIdbJ61akjlPZM/N8vL9zJZcw8qFmko0EY8RNmF1aUNE7qEcfaEyQNu/tlmIsUeYl5kPbZgL8fUiKMssPunn4ciffRsstEIcRbvtkVUdDKvr5QdQdf5J0o167t5vXBvctqzggQXUYOOBv8Cb9G9W5NcGibg9J3OCd7JMZTNGPV6gFAtga/WJL; page_uid=idY26sprvTVssudbzPwssssssI4-486433; _naver_usersession_=SXc2E3wZ6W9q/0SVHj+cMQ=='}

    for d in pd.date_range(startdate, enddate):
        str_d = d.strftime("%Y.%m.%d")
        page = 1
        print(str_d)
        while True:
            start = (page - 1) * 10 + 1
            print(page)
            URL = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query={0}&sort=2&photo=0&field=0&pd=3&ds={1}&de={2}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&office_category=0&service_area=0&nso=so:r,p:from{3}to{4},a:all&start={5}".format(keyword, str_d, str_d, str_d.replace(".",""), str_d.replace(".",""), start)

            res = requests.get(URL, headers=h)
            soup = BeautifulSoup(res.text, "html.parser")

            if soup.select_one(".api_noresult_wrap"):
                break

            news_list = soup.select("ul.list_news li")

            for item in news_list:
                if len(item.select("div.info_group a")) == 2:
                    li.append(get_news(item.select("div.info_group a")[1]['href']))
            page = page + 1

    df = pd.DataFrame(li, columns=['title', 'date', 'media', 'content', 'url'])
    return df

# Call your get_news_list function with the desired keyword and date range
df = get_news_list('테슬라', '2022.01.01', '2022.01.31')

# Save the DataFrame to a CSV file
df.to_csv('TeslaNewsData-2022-Jan.csv', index=False)
