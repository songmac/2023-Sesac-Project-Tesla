# <뉴스 크롤링 데이터 전처리 및 저장>
# 전처리 과정 설명 : 결측치 제거 -> 날짜 형식 변경 -> Null값 공백처리 -> df 행 공백 제거 
# (계속) -> 불용어처리 -> 주식 브리핑(140자 내외) 기사 제외

import pandas as pd
import csvfile as csvfile
import cleaningData as cleaningData


# 병합된 데이터 프레임 받아오기
news_dirpath = './selena_merge/data/original_data/news_data'
merged_df = csvfile.merge_csv(news_dirpath)

# 병합된 데이터 프레임을 파일로 저장
merged_filename = news_dirpath + '/merged_news_data_Oct_to_Dec.csv'
merged_df.to_csv(merged_filename, index=False, encoding='utf-8-sig')

# 저장된 병합 파일 불러오기
df = pd.read_csv(merged_filename)
print(f'원본 뉴스 dataframe shape : ', df.shape)

#결측치 제거
df = df.dropna(axis=0)
print(f'결측치 제거 후 dataframe shape : ', df.shape)

print("-------------------------불필요한 정보 제거--------------------------------")

#media(신문매체이름), Unnamed 열 제거
#df.drop(['media','Unnamed: 0'], axis=1, inplace = True)
#print(df.head(10))

# 컬럼명 변경 (주식데이터와 merge 하기 위해)
df = df.rename(columns={'date' : '날짜'})

#datetime으로 타입 변경
df['date'] = pd.to_datetime(df['날짜'])
#print(df[:10])

# NaN 값을 빈 문자열로 대체
df['content_data'] = df['content'].fillna('').astype(str)

# 공백 처리
df['content_data'] = cleaningData.trim_pattern_whitespace(df['content_data'])
#print(df[:10])

#불용어 처리
df['content_data'] = df['content_data'].map(cleaningData.clean_byline)
#print(df[:10])

#content 기사 길이가 140자 이하인 경우 제외
df = df.loc[df['content_data'].str.len() > 140]
print(f'길이가 140자 이하인 기사 제외 후 : ', df.shape)

#전처리 된 파일 저장
news_savepath = './selena_merge/data/preprocessing_data/'
news_savename = 'telsa_preprosessing_data_Oct_to_Dec'
csvfile.save_csv(df[['날짜','content_data']], news_savepath, news_savename)