from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel, TfidfModel
from gensim.models import ldamulticore
import pandas as pd
import numpy as np
import csvfile, modeling

print("---------------------테슬라 주식 데이터 Dataframe ------------------------")

# 테슬라 주식 데이터 Dataframe
# 전체 날짜
# teslaFilePath = './merge/data/'
# teslaFileName = 'merge_stock_data'

stockFilePath = './stock_data/'
stockFileName = 'TSLA_DATA_2023_daily'

#테슬라 주식 dataFrame
stocks_df = pd.DataFrame()
stocks_df = csvfile.call_csv(stockFilePath, stockFileName)

#datetime으로 타입 변환
stocks_df['날짜'] = pd.to_datetime(stocks_df['날짜'])
#print('주식 데이터 shape : ', stocks_df.shape)

#거래량 M/B를 제외한 숫자로만 표기습을 진행함
stocks_df['거래량'] = pd.to_numeric(stocks_df['거래량'].str.replace('M', ''))

#날짜와 거래량 추출 : stock_df
stock_df = stocks_df[['날짜','거래량']]
print(stock_df)

print("---------------------테슬라 기사 데이터 Dataframe ------------------------")

newsFilePath = './yumi/data/'
newsFileName = 'cleanWords'

#테슬라 뉴스 dataFrame
words_df = pd.DataFrame()
words_df = csvfile.call_csv(newsFilePath, newsFileName)

#주식 데이터와 열 이름 통일
words_df = words_df.rename(columns={'date' : '날짜'})

#datetime으로 타입 변환
words_df['날짜'] = pd.to_datetime(words_df['날짜'])

#기사 데이터 날짜별 기사 수 추출
news_cnt_daily = words_df.groupby(words_df['날짜']).count()['nouns_content']
#print(news_cnt_daily)

daily_news_count = news_cnt_daily.reset_index()
daily_news_count.columns = ['날짜', '기사갯수']
print(daily_news_count.info())

print("---------------------기사와 주식 병합 Dataframe ------------------------")
# 주식 데이터와 기사 데이터를 병합
data_df = pd.merge(stock_df, daily_news_count, how='outer', on='날짜')
#print(data_df.info())

#결측지 제거 : 주가가 없는 날짜 제거 (주말)
data_df = data_df.dropna()
print(data_df.info())

#날짜별 기사개수/주식거래량 수
stock_daily_volume = data_df['거래량']
news_daily_cnt = data_df['기사갯수']

#총 기사개수/거래량 수
#stock_volume = data_df['거래량'].sum()
#news_cnt = data_df['기사갯수'].sum()
#print('2023년 기사 개수 :', news_cnt)

print('날짜별 기사개수 : {}, 날짜별 주식 거래양 수 : {}'.format(news_daily_cnt, stock_daily_volume))

print("---------------------라쏘 회귀 ------------------------")

# 라쏘 회귀  : 
# 선형 회귀는 비용함수인 mse를 최소하하는 방향으로 머신러닝 모델이 학습을 진행
# TF-IDF는 단어의 빈도수(TF)와 단어가 들어있는 문서 수의 반비례 하는 수(IDF)를 곱한값
# 기사 수(news_cnt) : X, 주식거래량(stock_volume) : y
# 각 데이터를 StandardScaler/MinMaxScaler로 표준화하여 모델링

X = data_df['기사갯수'].values.reshape(-1,1)
y = data_df['거래량'].values.reshape(-1,1)
alpha = 0.001
n_splits = 5
alphas = [0.001, 0.01, 0.1, 1, 10, 100]

#라쏘회귀 실행
print(modeling.LASSO_KFold(X, y, alpha, n_splits))

# 최적의 alpha 찾기
print(modeling.optimize_alpha(X, y, alphas, n_splits))

print("---------------------LDA 모델링------------------------")
#딕셔너리 생성 : 다시하기 
dic = Dictionary()
#clean_words = words_df['nouns_content']
clean_words = words_df['nouns_content'].apply(lambda x: x.split())
id2word = Dictionary(clean_words)
print(id2word)

corpus_TDM = []
for doc in clean_words:
  #print(doc)
  result = id2word.doc2bow(doc)
  corpus_TDM.append(result)

#tfidf로 벡터화 적용
tfidf = TfidfModel(corpus_TDM)
corpus_TFIDF = tfidf[corpus_TDM]

#LDA 모델링
n = 30 #토픽의 개수
lda = ldamulticore.LdaMulticore(corpus=corpus_TFIDF,
                                id2word=id2word,
                                num_topics=n,
                                random_state=100,
                                passes=15,
                                workers=4)

for t in lda.print_topics():
  print(t[0],":",t[1])

