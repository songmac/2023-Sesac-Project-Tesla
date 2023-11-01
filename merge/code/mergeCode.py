import pandas as pd
import os

#cvs file처리하는 모듈

#2020 ~ 2023년으로 시작하는 csv 파일 전부 merge
#이 코드는 년도별 merge할 파일과 merge된 저장된 파일이 동일한 폴더 위치에 저장됨
#dirpath : 년도별 merge할 파일 위치와 저장할 위치 savefileName: 저장할 파일 이름
def merge_csv(dirpath, savefileName):
    
    file_list = os.listdir(dirpath)
    file_list_csv = [file for file in file_list if file.endswith('.csv')]

    merged_df = pd.DataFrame()
    
    for file in file_list_csv:
        # 파일명에서 연도 정보 추출 (예: "2022_01_news_data.csv")
        year = file.split('_')[0]
        #2020 ~ 2023년도로 시작하는 파일명만 merge
        if year in ['2023','2022','2021','2020'] :
            print(file)
            df = pd.read_csv(dirpath + file, dtype='object')
            merged_df = merged_df._append(df)
            
    #동일한 폴더에 병합한 csv 파일 저장
    merged_df.to_csv(dirpath + savefileName + ".csv", index=False, encoding='utf-8-sig')
    
#불려온 cvs 파일을 dataframe으로 리턴   
#dirpath : cvs파일가 있는 위치  fileName : 불려올 파일 이름
def call_csv(dirpath, fileName):
    merged_file = dirpath + fileName + '.csv'
    df = pd.read_csv(merged_file)
    return df

#csv 파일 저장
#df: 저장할 dataframe dirpath : 저장할 위치 fileName : 저장할 파일이름
def save_file(df, dirpath, savefileName) :
    fileFormat = '.csv'
    df.to_csv(dirpath + savefileName + fileFormat , encoding='utf-8-sig')

#csv 파일 저장
#df: 저장할 dataframe dirpath : 저장할 위치 fileName : 저장할 파일이름
def save_file(df, dirpath, savefileName) :
    fileFormat = '.csv'
    df.to_csv(dirpath + savefileName + fileFormat , encoding='utf-8-sig')

#테슬라 주식 파일 읽어오기
#dirpath : 테슬라 파일 주식 위치
#savepath : 저장할 파일 위치
# fileName : 저장할 파일 이름
def daily_stock_merge_csv(dirpath,savepath,fileName):
    
    file_list = os.listdir(dirpath)
    file_list_csv = [file for file in file_list if file.endswith('.csv')]

    merged_df = pd.DataFrame()
    
    for file in file_list_csv:
        # 파일명에서 연도 정보 추출 (예: "2022_01_news_data.csv")
        #2020 ~ 2023년도 daily가 포함된 파일명만 merge
        if 'daily' in file and ['2023','2022','2021','2020']:
            print(file)
            df = pd.read_csv(dirpath + file, dtype='object')
            merged_df = merged_df._append(df)
    #동일한 폴더에 병합한 csv 파일 저장
    merged_df.to_csv(savepath + fileName + ".csv", index=False, encoding='utf-8-sig')