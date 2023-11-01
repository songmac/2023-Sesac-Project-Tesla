import os
import pandas as pd
from collections import Counter
from konlpy.tag import Mecab
import csvfile, cleaningData

# 상위 10개 단어 추출
def word_counter(wordArr):
    all_word = [word for words in wordArr for word in words]
    word_count = Counter(all_word)
    most_commos_words = word_count.most_common(20)
    return most_commos_words

#mecab 실행
#existing_path = os.environ.get('PATH', '')
# 추가할 디렉토리를 설정
#new_path = r'C:\mecab\bin'
# PATH 환경변수에 새 디렉토리를 추가
#os.environ['PATH'] = new_path + os.pathsep + existing_path
# 변경된 PATH 값을 확인
#print(os.environ['PATH'])

#전처리된 파일 읽어 오기 
filepath = './yumi/data/'
prepro_fileName = 'telsa_preprosessing'
words_df = csvfile.call_csv(filepath, prepro_fileName)
#print(f'전처리한 날짜, 본문 shape : ', df.shape)

words_df.drop('Unnamed: 0', axis=1, inplace = True)
#print(words_df.shape, words_df)

#공백으로 본문 내용 split
words_list = words_df['content_data'].str.split()
word_counter(words_list)
#print(words_list[:10])

#기사 내용을 토큰화
docs = words_df['content_data']

#공백으로 토큰화
tokenized_docs = []
for doc in docs:
  tokenized_docs.append(doc.split())
#print(word_counter(tokenized_docs))

#품사부착 (PoS Tagging)
#명사만 추출 
#VSCODE시 Mecab에 dic path 넣어주기
mecab = Mecab('C:\mecab\share\mecab-ko-dic')
words_df['nouns_content'] = words_df['content_data'].apply(lambda x: mecab.nouns(x))
print(words_df['nouns_content'][:10])

#word_df를 리스트로 변환
words_list = words_df['nouns_content'].tolist()

#불용어처리
words_df['nouns_content'] = words_df['nouns_content'].map(cleaningData.remove_korean_stopwords)
clean_words = words_df['nouns_content']
print('불용어 제거 후 : ', clean_words[:20])

# 최빈어를 조회하여 불용어 제거 대상 선정
most_common_tag = []
for token in clean_words:
  most_common_tag += token
print(Counter(most_common_tag).most_common(30))

#불용어 제거한 파일 저장
clean_fileName = 'cleanWords'
csvfile.save_file(words_df, filepath, clean_fileName)







