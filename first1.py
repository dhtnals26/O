import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 연령별 인구 현황 분석")

# CSV 파일 경로
file_path = "202505_202505_연령별인구현황_월간.csv"

# 데이터 불러오기 (EUC-KR 인코딩)
df = pd.read_csv(file_path, encoding='euc-kr')

# 데이터 미리보기
st.subheader("📄 원본 데이터 미리보기")
st.dataframe(df)

# 연령별 열 추출
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
total_pop_column = [col for col in df.columns if '총인구수' in col][0]  # 총인구수 컬럼 자동 식별

# 열 이름에서 연령만 추출
new_column_names = {col: col.replace('2025년05월_계_', '').replace('세', '') for col in age_columns}
df_renamed = df.rename(columns=new_column_names)

# 총인구수 숫자 변환
df_renamed[total_pop_column] = pd.to_numeric(df_renamed[total_pop_column], errors='coerce')

# 상위 5개 행정구역 추출
top5_df = df_renamed.nlargest(5, total_pop_column)

# 연령별 인구 데이터 추출
age_only_cols = list(new_column_names.values())
region_col = '행정구역' if '행정구역' in top5_df.columns else '행정기관'

df_top5_age = top5_df[[region_col] + age_only_cols].copy()
df_top5_age.set_index(region_col, inplace=True)
df_top5_age = df_top5_age.T  # 전치

# 숫자로 변환
df_top5_age = df_top5_age.apply(pd.to_numeric, errors='coerce')

# 시각화
st.subheader("📈 상위 5개 지역 연령별 인구 분포")
st.line_chart(df_top5_age)

# 상위 5개 행정구역 정보 표시
st.subheader("🏙️ 총인구수 기준 상위 5개 지역")
st.dataframe(top5_df[[region_col, total_pop_column]])
