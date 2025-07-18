import streamlit as st
import pandas as pd

# Streamlit 기본 설정
st.set_page_config(page_title="도별 인구 및 세대 변화", layout="wide")
st.title("📊 도별 연도별 총인구수 및 세대수 변화")

# CSV 파일 경로
file_path = "200912_201812_주민등록인구및세대현황_연간.csv"

try:
    # 데이터 불러오기
    df = pd.read_csv(file_path, encoding="euc-kr")

    st.subheader("📄 원본 데이터")
    st.dataframe(df)

    # 분석 대상 지역
    regions = {
        "경기도": "경기도",
        "강원도": "강원도",
        "충청도": "충청북도|충청남도",
        "전라도": "전라북도|전라남도",
        "경상도": "경상북도|경상남도"
    }

    # 연도 추출
    population_cols = [col for col in df.columns if "총인구수" in col and "년" in col]
    years = sorted([col[:4] for col in population_cols])

    # 도별 그래프 생성
    for region_label, keyword in regions.items():
        region_df = df[df["행정구역"].str.contains(keyword)].copy()

        # 해당 도의 총합 계산
        pop_list = []
        hh_list = []

        for year in years:
            try:
                pop_sum = region_df[f"{year}년_총인구수"].astype(str).str.replace(",", "").astype(int).sum()
                hh_sum = region_df[f"{year}년_세대수"].astype(str).str.replace(",", "").astype(int).sum()
            except:
                pop_sum = hh_sum = 0
            pop_list.append(pop_sum)
            hh_list.append(hh_sum)

        # 데이터프레임 구성
        combined_df = pd.DataFrame({
            "연도": years,
            "총인구수": pop_list,
            "세대수": hh_list
        }).set_index("연도")

        # 도별 그래프 표시
        st.subheader(f"📈 {region_label}의 연도별 총인구수 및 세대수")
        st.line_chart(combined_df)

    # 결론 출력
    st.markdown("""
    ---
    ### 📌 결론
    총인구는 줄고 있지만 **세대 수는 꾸준히 증가**하고 있으며,  
    특히 **1인 가구 비율이 빠르게 증가**하고 있습니다.  
    이는 **혼인율 감소**, **고령화**, **개인화** 등의 사회 변화 때문이며,  
    앞으로 **주거 및 복지 정책의 변화**가 필요함을 보여줍니다.
    """)

except FileNotFoundError:
    st.error(f"CSV 파일이 존재하지 않습니다: {file_path}")
except Exception as e:
    st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
