import streamlit as st
import pandas as pd
import folium
from folium import Circle
from streamlit.components.v1 import html
import re

# 제목
st.title("2025년 5월 기준 연령별 인구 현황")

# CSV 파일 로딩
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 괄호 제거 (행정구역명 정리)
df['행정구역'] = df['행정구역'].apply(lambda x: re.sub(r'\(.*\)', '', x).strip())

# 총인구수 정리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '', regex=False).astype(int)

# 연령 관련 열 추출 및 이름 정리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 총인구수 기준 상위 5개 행정구역
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 위도 경도 정보 매핑 (직접 지정)
location_dict = {
    '서울특별시': [37.5665, 126.9780],
    '부산광역시': [35.1796, 129.0756],
    '인천광역시': [37.4563, 126.7052],
    '대구광역시': [35.8722, 128.6025],
    '대전광역시': [36.3504, 127.3845],
    '광주광역시': [35.1595, 126.8526],
    '울산광역시': [35.5384, 129.3114],
    '경기도 수원시': [37.2636, 127.0286],
    '경상북도 포항시': [36.0190, 129.3435],
    '전라북도 전주시': [35.8242, 127.1479],
    '충청남도 천안시': [36.8151, 127.1139],
    '강원도 춘천시': [37.8813, 127.7298],
}

# 위도/경도 추가
top5_df['위도'] = top5_df['행정구역'].apply(lambda x: location_dict.get(x, [None, None])[0])
top5_df['경도'] = top5_df['행정구역'].apply(lambda x: location_dict.get(x, [None, None])[1])

# 지도 표시
st.subheader("🗺️ 상위 5개 행정구역 위치 (Folium 지도)")

# 지도 중심 설정
center_lat = top5_df['위도'].mean()
center_lon = top5_df['경도'].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

# 지도에 핑크색 반투명 원 추가
for _, row in top5_df.iterrows():
    if pd.notnull(row['위도']) and pd.notnull(row['경도']):
        Circle(
            location=[row['위도'], row['경도']],
            radius=15000,
            color='pink',
            fill=True,
            fill_color='pink',
            fill_opacity=0.5,
            popup=f"{row['행정구역']}<br>총인구수: {row['총인구수']:,}"
        ).add_to(m)

# 지도 출력
folium_html = m._repr_html_()
html(folium_html, height=500)

# 원본 데이터 테이블
st.subheader("📊 원본 데이터 (상위 5개 행정구역)")
st.dataframe(top5_df[['행정구역', '총인구수']])

# 선그래프 출력
st.subheader("📈 상위 5개 행정구역 연령별 인구 변화")
age_columns_only = top5_df.columns[2:-2]  # 마지막 2개는 위경도

for index, row in top5_df.iterrows():
    st.markdown(f"### {row['행정구역']}")
    age_data = row[age_columns_only].astype(str).str.replace(',', '', regex=False).astype(int)
    age_df = pd.DataFrame({
        '연령': age_columns_only,
        '인구수': age_data.values
    }).set_index('연령')
    st.line_chart(age_df)
