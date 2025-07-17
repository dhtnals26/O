import streamlit as st
import pandas as pd

st.title("연도별 주민등록 인구 현황 (시도별)")

# CSV 파일 불러오기
try:
    df = pd.read_csv("201912_202412_주민등록인구및세대현황_연간.csv", encoding="EUC-KR", skiprows=1)
except Exception as e:
    st.error(f"CSV 파일을 불러오는 데 실패했습니다: {e}")
    st.stop()

# 컬럼 이름 정리
df = df.rename(columns={df.columns[0]: "구분"})

# '총인구' 행 제거, '전국 합계' 등 시도만 남기기
df = df[~df["구분"].str.contains("총인구")]

# 시도만 필터링 (예: '서울특별시', '부산광역시' 등)
df = df[~df["구분"].str.contains("계")]

# 인구 데이터 전처리
df = df.set_index("구분").T  # 연도를 행으로 만들기
df.index.name = "연도"

# 연도 문자열 처리 (예: "2019년" -> 2019)
df.index = df.index.str.extract(r"(\d{4})")[0]
df = df.dropna()
df.index = df.index.astype(int)
df = df.sort_index()  # 연도 순으로 정렬

# 쉼표 제거하고 숫자로 변환
df = df.apply(lambda x: x.str.replace(",", "").astype(float))

# 원본 데이터 표시
st.subheader("원본 데이터 (전처리 후)")
st.dataframe(df)

# 시도별 그래프
st.subheader("시도별 인구 변화")

for col in df.columns:
    st.write(f"📈 {col}")
    st.line_chart(df[[col]])

# 전체 시도 겹친 그래프
st.subheader("전체 시도 인구 변화 비교")
st.line_chart(df)
