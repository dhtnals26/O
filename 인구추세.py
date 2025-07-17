import streamlit as st
import pandas as pd

st.title("연도별 주민등록 인구 현황 (시도별)")

# CSV 파일 불러오기
try:
    df = pd.read_csv("201912_202412_주민등록인구및세대현황_연간.csv", encoding="EUC-KR", skiprows=1)
except Exception as e:
    st.error(f"CSV 파일을 불러오는 데 실패했습니다: {e}")
    st.stop()

# 첫 번째 열 이름이 "행정구역(1)" 또는 "행정구역"과 유사 → 이 열이 '지역' 정보
지역_컬럼명 = df.columns[0]

# 연도 정보가 인덱스로 존재
df = df.rename(columns={지역_컬럼명: "구분"})
df = df[df["구분"].str.contains("총인구") == False]  # '총인구'로 시작하는 행 제거

# 필요한 정보만 추출 (시도 행만)
시도_행 = df["구분"].str.contains("합계") == False
df = df[시도_행]

# 연도별 인구 추출
df = df.set_index("구분").T  # Transpose해서 연도 기준으로 회전
df.index.name = "연도"

# 숫자형으로 변환 (쉼표 제거)
df = df.apply(lambda x: x.str.replace(",", "").astype(float))

# 원본 데이터 표시
st.subheader("원본 데이터 (전처리 후)")
st.dataframe(df)

# 각 시도별 그래프 출력
st.subheader("시도별 인구 변화")

for col in df.columns:
    st.write(f"📈 {col}")
    st.line_chart(df[[col]])

# 전체 시도 겹친 선 그래프
st.subheader("전체 시도 인구 변화 비교")
st.line_chart(df)
