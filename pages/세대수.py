import streamlit as st
import pandas as pd

# Streamlit 페이지 설정
st.set_page_config(page_title="지역별 인구 및 세대 변화", layout="wide")
st.title("📊 지역별 연도별 총인구수 및 세대수 변화")

# CSV 파일 경로 (현재 디렉터리에 있다고 가정)
file_path = "200912_201812_주민등록인구및세대현황_연간.csv"

try:
    # 데이터 불러오기
    df = pd.read_csv(file_path, encoding="euc-kr")

    # 원본 데이터 표시
    st.subheader("📄 원본 데이터")
    st.dataframe(df)

    # 분석할 지역 목록
    regions = ["경기도", "강원도", "전라", "경상", "충청"]

    # 지역 필터링
    df_regions = df[df["행정구역"].str.contains("|".join(regions))].copy()

    # 총인구수와 세대수 열 추출
    population_cols = [col for col in df.columns if "총인구수" in col and "년" in col]
    household_cols = [col for col in df.columns if "세대수" in col and "년" in col]
    years = sorted(list(set([col[:4] for col in population_cols])))

    # 결과 데이터프레임 초기화
    data_population = pd.DataFrame(index=years)
    data_household = pd.DataFrame(index=years)

    # 지역별 데이터 정리
    for _, row in df_regions.iterrows():
        region_name = row["행정구역"]
        if "전라" in region_name:
            label = "전라도"
        elif "경상" in region_name:
            label = "경상도"
        elif "충청" in region_name:
            label = "충청도"
        else:
            label = region_name  # 경기도, 강원도

        # 총인구수
        pop_values = [int(str(row[f"{year}년_총인구수"]).replace(",", "").strip()) for year in years]
        data_population[label] = pop_values

        # 세대수
        household_values = [int(str(row[f"{year}년_세대수"]).replace(",", "").strip()) for year in years]
        data_household[label] = household_values

    # 인덱스 정리
    data_population.index.name = "연도"
    data_household.index.name = "연도"

    # 시각화
    st.subheader("👨‍👩‍👧‍👦 연도별 총인구수 변화 (지역별)")
    st.line_chart(data_population)

    st.subheader("🏠 연도별 세대수 변화 (지역별)")
    st.line_chart(data_household)

    # 결론
    st.markdown("""
    ### 📌 결론
    총인구는 줄고 있지만 **세대 수는 계속 증가**하고 있으며,  
    특히 **1인 가구 비율이 빠르게 증가**하고 있습니다.  
    이는 **혼인율 감소, 고령화, 개인화** 등의 사회 변화 때문이며,  
    앞으로 **주거·복지 정책의 변화**가 필요함을 보여줍니다.
    """)

except FileNotFoundError:
    st.error(f"CSV 파일이 경로에 존재하지 않습니다: {file_path}")
except Exception as e:
    st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
