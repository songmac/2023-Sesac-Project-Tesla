#vscode에서 진행
import os

# 기존 PATH 환경변수 값을 가져옵니다.
existing_path = os.environ.get('PATH', '')

# 추가할 디렉토리를 설정합니다.
new_path = r'C:\mecab\bin'

# PATH 환경변수에 새 디렉토리를 추가합니다.
os.environ['PATH'] = new_path + os.pathsep + existing_path

# 변경된 PATH 값을 확인합니다.
print(os.environ['PATH'])



# #cmd 창에서 설치/아나콘다에서 안함
# pip install mecab-ko-msvc mecab-ko-dic-msvc

# #최신버전 인스톨
# pip install --upgrade mecab-python