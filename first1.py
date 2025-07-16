import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 연령별 인구 현황 분석")

# CSV 파일 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 데이터 미리보기
st.subheader("📄 원본 데이터 미리보기")
st.dataframe(df)

# 연령별 열 이름 정리
df_renamed = df.copy()
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_')]

# 열 이름에서 연령 숫자만 남기기
new_column_names = {col: col.replace('2025년05월_계_', '').replace('세', '') for col in age_columns}
df_renamed.rename(columns=new_column_names, inplace=True)

# 상위 5개 행정구역 추출 (총인구수 기준)
df_top5 = df_renamed.nlargest(5, '총인구수')

# 연령별 인구 데이터만 추출 (세로로 나타나게 전치)
df_top5_age = df_top5[['행정구역'] + list(new_column_names.values())]
df_top5_age.set_index('행정구역', inplace=True)
df_top5_age = df_top5_age.T  # 전치: 연령을 세로축으로

# 정수형으로 변환
df_top5_age = df_top5_age.apply(pd.to_numeric, errors='coerce')

# 시각화
st.subheader("📈 상위 5개 지역 연령별 인구 분포")
st.line_chart(df_top5_age)

# 상위 5개 지역 정보
st.subheader("🏙️ 총인구수 기준 상위 5개 지역")
st.dataframe(df_top5[['행정구역', '총인구수']])
