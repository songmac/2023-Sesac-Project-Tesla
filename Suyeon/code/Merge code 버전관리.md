# [colab, vscode] Merge code 버전 관리

### V1.0 : 각 실행 창 마다 결과 확인
- 수집정보 :  title, date, media, content, url
- cvs 파일명 : [2022-Jan]news_data_preprocessing 

### V1.3 : 실행 한번에 뉴스 크롤링 및 csv 파일 저장 가능하도록 수정
- 수집정보 :  title, date, content (media, url 삭제) 
- cvs 파일명 : [2022-Jan]news_data_preprocessing -> [2022-Jan]news_data_cleansing으로 수정

----------------------------------------------------------------- Data Collecting & Cleansing

### V1.5 : 토큰화, LDA 분석 정리
- colab은 완료함
- vscode는 konlpy 설치 이슈 발생하여 해결중

### V1.8 : LDA, LASSO, K-Fold 코드 rough 하게 작성하여 완성본은 아님

----------------------------------------------------------------- Data Preprocessing & Analysis

### 구현중인 내용
- colab → vscode로 옮기기
- mecab 적용하기
- 병렬처리 적용하기
- K-fold 구현하기
- FPE, FVE 수식 설정하고 프로그래밍으로 구현하기 (시각화 그래프 그리기)
- 멤버들과 소스 병합 및 정리하기
- 엑셀파일 병합 코드 추가 및 1년 데이터 분석해보기

### 발표 이후 진행할 수 있는 내용
- (추후) 트위터 감정분석 → 주가 변동 예측하기
