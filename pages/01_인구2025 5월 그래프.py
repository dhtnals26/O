import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="상위 5개 행정구역 인구 지도", layout="wide")

st.title("🗺️ 상위 5개 행정구역 인구수 지도 시각화")

# CSV 파일 읽기
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 괄호 안 숫자 제거 (예: 경기도 수원시(41110) → 경기도 수원시)
df['행정구역'] = df['행정구역'].str.replace(r"\s*\(\d+\)", "", regex=True).str.strip()

# 총인구수 컬럼 정리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 상위 5개 지역 추출
top5_df = df.sort_values(by='총인구수', ascending=False).head(5)

# 행정구역명에 맞는 위도/경도 수동 입력 (정확도 중요)
region_coords = {
    "경기도": [37.4138, 127.5183],
    "서울특별시": [37.5665, 126.9780],
    "부산광역시": [35.1796, 129.0756],
    "경상남도": [35.4606, 128.2132],
    "인천광역시": [37.4563, 126.7052]
}

# 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 각 지역에 원 추가
for _, row in top5_df.iterrows():
    region = row['행정구역']
    population = row['총인구수']
    coords = region_coords.get(region)

    if coords:
        folium.Circle(
            location=coords,
            radius=population / 30,  # 적절한 비율로 원 크기 조절
            color='deeppink',
            fill=True,
            fill_color='lightpink',
            fill_opacity=0.5,
            popup=folium.Popup(f"{region} : {population:,}명", max_width=250),
            tooltip=region
        ).add_to(m)

# 지도 출력
st.subheader("🗺️ 지도에서 인구수 확인")
st_folium(m, width=900, height=600)

# 데이터 출력
st.subheader("📊 상위 5개 행정구역 데이터")
st.dataframe(top5_df[['행정구역', '총인구수']])
