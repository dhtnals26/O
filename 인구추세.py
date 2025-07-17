import streamlit as st
import pandas as pd

# 제목
st.title("연도별 주민등록 인구 현황")

# CSV 파일 불러오기
try:
    df = pd.read_csv("201912_202412_주민등록인구및세대현황_연간.csv", encoding='EUC-KR')
except UnicodeDecodeError:
    st.error("CSV 파일을 불러오는 데 실패했습니다. 인코딩을 확인해주세요.")
    st.stop()

# 원본 데이터 표시
st.subheader("원본 데이터")
st.dataframe(df)

# 데이터 전처리
# 연도와 전체 인구 컬럼만 추출 (예시: "2020년", "총인구수 (명)" 등)
# 아래는 컬럼명을 확인 후 조정이 필요할 수 있음
try:
    # 연도 컬럼 이름 찾기
    year_col = [col for col in df.columns if "연도" in col or "기준" in col][0]
    pop_col = [col for col in df.columns if "총인구" in col and "명" in col][0]

    # 연도와 인구 수로 구성된 새로운 DataFrame 생성
    pop_df = df[[year_col, pop_col]].copy()
    pop_df = pop_df.rename(columns={year_col: "연도", pop_col: "인구수"})
    pop_df["연도"] = pop_df["연도"].astype(str)
    pop_df = pop_df.set_index("연도")
    
    # 선 그래프 시각화
    st.subheader("연도별 인구 변화")
    st.line_chart(pop_df)

except Exception as e:
    st.error(f"데이터 전처리 중 오류가 발생했습니다: {e}")
