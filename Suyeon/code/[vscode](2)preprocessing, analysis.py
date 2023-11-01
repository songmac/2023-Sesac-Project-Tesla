# 모듈 임포트 선언
import os
import numpy as np
import pandas as pd

import re, unicodedata
from string import whitespace

import time
from multiprocessing import Pool

from konlpy.tag import Okt
from gensim import corpora
from gensim.models import LdaModel, TfidfModel, CoherenceModel

from sklearn.linear_model import Lasso
from sklearn.model_selection import KFold, train_test_split
from sklearn.preprocessing import StandardScaler
# import pyLDAvis.gensim



# 크롤링 & 클렌징한 csv 파일 불러오기
df = pd.read_csv(r'C:\Users\User\project\SESAC\Team-SeSAC\Team_SeSAC\Suyeon\data\cleansing\[2022-Jan]news_data_cleansing.csv')

# 형태소 분석기 초기화
okt = Okt()

# 불용어 리스트 정의
stop_words = ["것", "수", "이", "그", "를", "를", "등", "과", "에", "가", '때', '의', '및', '월', '위', '일', '억', '년', '원', '지난해', '를', '것', '등','차','올해','챗'
              '위', '가', '조', '의', '및','약','수','주','기자','만','이','중','말','마하','미']

# 텍스트 데이터를 리스트로 변환
documents = df['content'].tolist()

# 각 문서를 형태소 분석 및 토큰화하고 불용어 제거
tokenized_documents = []
for document in documents:
    # 형태소 분석 수행 후 명사만 선택 (원하는 형태소 선택 가능)
    tokens = [word for word, pos in okt.pos(str(document)) if pos in ['Noun'] and word not in stop_words]
    tokenized_documents.append(tokens)

# 사전 (Dictionary) 생성
dictionary = corpora.Dictionary(tokenized_documents)



# Tfidf 모델 생성
tfidf = TfidfModel(dictionary=dictionary)
corpus = [dictionary.doc2bow(tokens) for tokens in tokenized_documents]


# LDA 모델 생성
lda_model = LdaModel(corpus, num_topics=30, id2word=dictionary, passes=15)


# LDA 모델 출력
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic #{idx}: {topic}")