import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 데이터 불러오기
file_path = "202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding="euc-kr")

# 원본 데이터 표시
st.subheader("📄 원본 데이터")
st.dataframe(df)

# 연령 관련 컬럼만 추출 (예: '2025년05월_계_0세' → '0세')
age_columns = [col for col in df.columns if col.startswith("2025년05월_계_")]
age_labels = [col.replace("2025년05월_계_", "").replace("세", "") for col in age_columns]

# 새로운 DataFrame 생성
df_age = df[["행정기관"] + age_columns + ["2025년05월_계_총인구수"]].copy()
df_age.columns = ["행정기관"] + age_labels + ["총인구수"]

# 총인구수 기준 상위 5개 지역 선택
df_age["총인구수"] = pd.to_numeric(df_age["총인구수"], errors="coerce")
top5 = df_age.nlargest(5, "총인구수")

# 숫자형으로 변환 (연령별 인구)
age_numeric = [col for col in top5.columns if col not in ["행정기관", "총인구수"]]
top5[age_numeric] = top5[age_numeric].apply(pd.to_numeric, errors="coerce")

# 데이터 변환: 연령별 인구를 행으로 변환
df_melted = top5.melt(id_vars="행정기관", value_vars=age_numeric,
                      var_name="연령", value_name="인구수")

# 피벗: 연령별로 지역별 인구수를 컬럼으로
df_pivot = df_melted.pivot(index="연령", columns="행정기관", values="인구수")
df_pivot = df_pivot.sort_index(key=lambda x: x.astype(int))  # 연령 순으로 정렬

# 시각화
st.subheader("📈 상위 5개 지역의 연령별 인구 변화")
st.line_chart(df_pivot)
