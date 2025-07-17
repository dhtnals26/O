import streamlit as st
import pandas as pd

st.title("연도별 주민등록 인구 현황 (시도별, 막대그래프)")

# CSV 불러오기
try:
    df_raw = pd.read_csv("201912_202412_주민등록인구및세대현황_연간.csv", encoding="EUC-KR")
except Exception as e:
    st.error(f"CSV 파일을 불러오는 중 오류 발생: {e}")
    st.stop()

# 첫 열 이름 정리
df_raw = df_raw.rename(columns={df_raw.columns[0]: "구분"})

# '총인구' 또는 '계'가 들어간 행 제거 (시도만 남기기)
df = df_raw[~df_raw["구분"].str.contains("총인구|계")]

# 전치: 연도를 인덱스로 만들기 위해 전환
df = df.set_index("구분").T
df.index.name = "연도"

# 연도 문자열 정리: '2019년' -> '2019'
df = df.reset_index()  # index -> column
df["연도"] = df["연도"].astype(str).str.extract(r"(\d{4})")  # 정규식 추출
df = df.dropna(subset=["연도"])  # 연도 추출 실패한 행 제거
df["연도"] = df["연도"].astype(int)
df = df.set_index("연도")
df = df.sort_index()  # 연도 순 정렬

# 쉼표 제거 및 숫자형 변환
def clean_num(val):
    try:
        return float(str(val).replace(",", ""))
    except:
        return None

df = df.applymap(clean_num)

# 원본 데이터 출력
st.subheader("원본 데이터 (전처리 후)")
st.dataframe(df)

# 각 시도별 막대그래프
st.subheader("시도별 인구 변화 (막대그래프)")
for col in df.columns:
    st.write(f"📊 {col}")
    st.bar_chart(df[[col]])

# 전체 시도 겹쳐보기
st.subheader("전체 시도 인구 변화 비교 (막대그래프)")
st.bar_chart(df)
