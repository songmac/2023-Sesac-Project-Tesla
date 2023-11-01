import pandas as pd
import os

#cvs file처리하는 모듈

#2020 ~ 2023년으로 시작하는 csv 파일 전부 merge
def merge_monthly_csv(dirpath,fileName):
    
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
    merged_df.to_csv(dirpath + fileName + ".csv", index=False, encoding='utf-8-sig')
    
#불려온 cvs 파일을 dataframe으로 리턴   
def call_csv(dirpath, fileName):
    merged_file = dirpath + fileName + '.csv'
    df = pd.read_csv(merged_file)
    return df

#csv 파일 저장
def save_file(df, dirpath, fileName) :
    fileFormat = '.csv'
    df.to_csv(dirpath + fileName + fileFormat , encoding='utf-8-sig')