import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 도별 연령별 인구 현황 분석")

# CSV 파일 경로
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 원본 데이터 미리보기
st.subheader("📄 원본 데이터 미리보기")
st.dataframe(df)

# 연령 관련 열 찾기
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
total_pop_column = [col for col in df.columns if '총인구수' in col][0]
region_col = '행정구역' if '행정구역' in df.columns else '행정기관'

# 연령 숫자만 남기도록 열 이름 전처리
age_col_map = {col: col.replace('2025년05월_계_', '').replace('세', '') for col in age_columns}
df.rename(columns=age_col_map, inplace=True)

# 총인구수 숫자 변환
df[total_pop_column] = pd.to_numeric(df[total_pop_column], errors='coerce')

# 도 이름 리스트
do_list = ['경기도', '경상', '전라', '충청', '강원']

# 각 도별 그래프 출력
for do in do_list:
    st.subheader(f"📍 {do} 지역 연령별 인구 분포")

    # 도 이름이 포함된 행정구역 필터링
    df_do = df[df[region_col].str.contains(do)]

    if df_do.empty:
        st.write(f"❌ {do}에 해당하는 데이터가 없습니다.")
        continue

    # 연령별 인구만 추출
    age_only_cols = list(age_col_map.values())
    df_do_age = df_do[[region_col] + age_only_cols].copy()
    df_do_age.set_index(region_col, inplace=True)
    df_do_age = df_do_age.T
    df_do_age = df_do_age.apply(pd.to_numeric, errors='coerce')

    # 시각화
    st.line_chart(df_do_age)
