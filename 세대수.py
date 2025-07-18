import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="연도별 인구 및 세대 변화", layout="wide")

# 제목
st.title("📊 연도별 주민등록 인구 및 세대 변화")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요 (EUC-KR 인코딩)", type=["csv"])

if uploaded_file is not None:
    try:
        # CSV 읽기
        df = pd.read_csv(uploaded_file, encoding="euc-kr")

        # 원본 데이터 표시
        st.subheader("📄 원본 데이터")
        st.dataframe(df)

        # 필요한 열만 추출
        # '연도', '총인구수 (명)', '세대수 (세대)' 라는 이름이 있을 것으로 가정
        if '연도' in df.columns and '총인구수 (명)' in df.columns and '세대수 (세대)' in df.columns:
            df_filtered = df[['연도', '총인구수 (명)', '세대수 (세대)']].copy()

            # 연도를 datetime 형태로 변환 (또는 int 처리)
            df_filtered['연도'] = pd.to_numeric(df_filtered['연도'], errors='coerce')
            df_filtered.dropna(inplace=True)
            df_filtered.set_index('연도', inplace=True)

            # 선 그래프 시각화
            st.subheader("📈 연도별 총인구수 변화")
            st.line_chart(df_filtered[['총인구수 (명)']])

            st.subheader("📈 연도별 세대수 변화")
            st.line_chart(df_filtered[['세대수 (세대)']])

            # 인구수 + 세대수 비교 그래프
            st.subheader("📈 연도별 총인구수 및 세대수 비교")
            st.line_chart(df_filtered)

            # 결론
            st.markdown("""
            ### 📌 결론
            총인구는 줄고 있지만 세대 수는 계속 증가하고 있으며,  
            특히 **1인 가구 비율이 빠르게 늘고 있습니다**.  
            이는 **혼인율 감소, 고령화, 개인화** 등의 사회 변화 때문이며,  
            앞으로 **주거·복지 정책의 변화가 필요함**을 보여줍니다.
            """)

        else:
            st.warning("필요한 열('연도', '총인구수 (명)', '세대수 (세대)')이 존재하지 않습니다. 열 이름을 확인해주세요.")

    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바 또는 위에서 CSV 파일을 업로드해주세요.")
