import pandas as pd
import csvfile, cleaningData
import re,unicodedata
import os


def clean_byline(text):
    # byline
    pattern_url = re.compile(r'(?:https?:\/\/)?[-_0-9a-z]+(?:\.[-_0-9a-z]+)+', flags=re.IGNORECASE)
    pattern_others = re.compile(r'\.([^\.]*(?:기자|특파원|지난해|교수|서울|사진|작가|뉴스|대표|논설|고문|주필|부문장|팀장|장관|원장|연구원|이사장|위원|실장|차장|부장|에세이|화백|사설|소장|단장|과장|기획자|큐레이터|저작권|평론가|©|©|ⓒ|\@|\/|=|:앞쪽_화살표:|무단|전재|재배포|금지|\[|\]|\(\))[^\.]*)$')
    pattern_onlyKorean = re.compile('[^ ㄱ-ㅣ가-힣]+') #한글과 띄어쓰기만 추출
    #result = pattern_email.sub('', text)
    result = pattern_url.sub('', text)
    result = pattern_others.sub('.', result)
    result = pattern_onlyKorean.sub('',result)
    # 본문 시작 전 꺽쇠로 쌓인 바이라인 제거
    pattern_bracket = re.compile(r'^((?:\[.+\])|(?:【.+】)|(?:<.+>)|(?:◆.+◆)\s)')
    result = pattern_bracket.sub(' ', result).strip()
    return result

# filepath = './yumi/data/'
# fileName = '23_merge_news_data'

# df = csvfile.call_csv(filepath, fileName)

# print(df.shape)

#  #불용어 처리 content열에 함수 적용
# df['content'] = df['content'].fillna('').astype(str).map(clean_byline)

# # 유니코드 문자 전처리 및 정규 표현식 사용
# pattern_whitespace = re.compile(r'\s+')
# #df['content'] = df['content'].str.replace(pattern_whitespace, ' ').map(lambda x: unicodedata.normalize('NFC', x)).str.strip()
# df['content'] = df['content'].fillna('').astype(str).str.replace(r'\s+', ' ', regex=True)

# #content 기사 길이가 140자 이하인 경우 제외
# df = df.loc[df['content'].str.len() > 140]
# df.shape

# df.drop(['Unnamed: 0'], axis=1, inplace = True)

# # 전처리한 데이터 csv 파일로 저장
# df.to_csv('2023_news_data_cleansing.csv', index=False, encoding='utf-8-sig')


def merge_stock_csv(dirpath,savepath,fileName):
    
    file_list = os.listdir(dirpath)
    file_list_csv = [file for file in file_list if file.endswith('.csv')]

    merged_df = pd.DataFrame()
    
    for file in file_list_csv:
        # 파일명에서 연도 정보 추출 (예: "2022_01_news_data.csv")
        #year = file.split('_')[0]
        #2020 ~ 2023년도로 시작하는 파일명만 merge
        if 'daily' in file and ['2023','2022','2021','2020']:
            print(file)
            df = pd.read_csv(dirpath + file, dtype='object')
            merged_df = merged_df._append(df)
    #동일한 폴더에 병합한 csv 파일 저장
    merged_df.to_csv(savepath + fileName + ".csv", index=False, encoding='utf-8-sig')


merge_filepath = './stock_data/'
fileName = 'merge_stock_data'
savepath = './merge/data/'

merge_stock_csv(merge_filepath,savepath,fileName)


