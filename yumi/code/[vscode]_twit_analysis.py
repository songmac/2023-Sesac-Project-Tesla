from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel, TfidfModel
from gensim.models import LdaMulticore
import multiprocessing
import pandas as pd
import numpy as np
import csvfile, modeling
import time

print("--------------------- 트위터 데이터 dataframe ------------------------")

filepath = './twitter_data/yearly_twitter_data/'
fileName = 'cleanTwitWords'

#테슬라 주식 dataFrame
words_df = pd.DataFrame()
words_df = csvfile.read_csv(filepath, fileName)
print(f'처리 전 : ', words_df.shape)

# # 'nouns' 열에 대해 빈 리스트를 제거
# words_df = words_df[words_df['nouns'].apply(lambda x: len(x) > 0)]
# print(f'빈리스트 제거 후 : ', words_df.shape)


print("---------------------트위터와 주식 병합 Dataframe ------------------------")



print("---------------------라쏘 회귀 ------------------------")


print("---------------------LDA 모델링------------------------")