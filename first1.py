import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 도별 상위 5개 지역 연령별 인구 분석")

# CSV 파일 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 원본 데이터 미리보기
st.subheader("📄 원본 데이터 미리보기")
st.dataframe(df)

# 열 이름 처리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and '세' in col]
total_pop_column = [col for col in df.columns if '총인구수' in col][0]
region_col = '행정구역' if '행정구역' in df.columns else '행정기관'

# 연령 숫자만 추출한 새 컬럼 이름으로 변경
age_col_map = {col: col.replace('2025년05월_계_', '').replace('세', '') for col in age_columns}
df = df.rename(columns=age_col_map)

# 총인구수 숫자 변환
df[total_pop_column] = pd.to_numeric(df[total_pop_column], errors='coerce')

# 도별 검색 키워드
do_keywords = {
    '경기도': '경기',
    '경상도': '경상',
    '전라도': '전라',
    '충청도': '충청',
    '강원도': '강원'
}

# 도별 처리
for do_name, keyword in do_keywords.items():
    st.subheader(f"📍 {do_name} - 총인구수 상위 5개 시군의 연령별 인구 분포")

    # 해당 도에 속한 지역 필터링
    df_do = df[df[region_col].str.contains(keyword)]

    if df_do.empty:
        st.warning(f"❌ {do_name}에 해당하는 데이터가 없습니다.")
        continue

    # 총인구수 상위 5개 시군 선택
    top5 = df_do.nlargest(5, total_pop_column)

    # 연령별 인구 데이터만 추출
    age_only_cols = list(age_col_map.values())
    df_top5_age = top5[[region_col] + age_only_cols].copy()
    df_top5_age.set_index(region_col, inplace=True)
    df_top5_age = df_top5_age.T
    df_top5_age = df_top5_age.apply(pd.to_numeric, errors='coerce')

    # 선 그래프 시각화
    st.line_chart(df_top5_age)

    # 상위 5개 지역 정보도 함께 출력
    st.caption(f"💡 {do_name} 내 총인구수 상위 5개 지역")
    st.dataframe(top5[[region_col, total_pop_column]])
