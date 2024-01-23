import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정 (예시 폰트 경로, 실제 경로로 변경)
plt.rcParams["font.family"] = "NanumBarunGothic"
plt.rcParams["axes.unicode_minus"] = False  # 음수 부호 표시

# 주식 종목 또는 토픽의 라벨 (x 축)
labels = ["주식1", "주식2", "주식3", "토픽1", "토픽2", "토픽3"]

# FPE 및 FVE 값 (y 축)
fpe_values = [0.27, 0.70, 0.51, 0.43]  # 예시 값, 실제 데이터에 맞게 수정
fve_values = [0.5, 0.6, 0.7, 0.8]     # 예시 값, 실제 데이터에 맞게 수정

# FPE 시각화 (bar plot)
plt.figure(figsize=(10, 6))
sns.barplot(x=labels[:len(fpe_values)], y=fpe_values, palette="Blues")
plt.ylim(0, 1)  # y 축 범위 설정 (0에서 1까지)
plt.xlabel("주식 종목 또는 토픽")
plt.ylabel("FPE 값")
plt.title("주식 종목 또는 토픽별 Fraction of Peaks Explained (FPE)")
plt.xticks(rotation=45)  # x 축 라벨 회전
plt.show()

# FVE 시각화 (bar plot)
plt.figure(figsize=(10, 6))
sns.barplot(x=labels[:len(fve_values)], y=fve_values, palette="Greens")
plt.ylim(0, 1)  # y 축 범위 설정 (0에서 1까지)
plt.xlabel("주식 종목 또는 토픽")
plt.ylabel("FVE 값")
plt.title("주식 종목 또는 토픽별 Fraction of Volume Explained (FVE)")
plt.xticks(rotation=45)  # x 축 라벨 회전
plt.show()
