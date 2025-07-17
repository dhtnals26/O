import streamlit as st
import pandas as pd
import pydeck as pdk

st.title("2025년 5월 기준 연령별 인구 현황")

# CSV 불러오기
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 전처리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 상위 5개 행정구역
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 예시용 위도/경도 (실제 데이터로 대체 필요)
location_dict = {
    '서울특별시': [37.5665, 126.9780],
    '부산광역시': [35.1796, 129.0756],
    '경기도 수원시': [37.2636, 127.0286],
    '인천광역시': [37.4563, 126.7052],
    '대구광역시': [35.8722, 128.6025],
    '대전광역시': [36.3504, 127.3845],
    '광주광역시': [35.1595, 126.8526],
    '울산광역시': [35.5384, 129.3114]
}

# 위경도 컬럼 추가
top5_df["lat"] = top5_df["행정구역"].apply(lambda x: location_dict.get(x, [None, None])[0])
top5_df["lon"] = top5_df["행정구역"].apply(lambda x: location_dict.get(x, [None, None])[1])
map_df = top5_df.dropna(subset=["lat", "lon"])

# 지도 표시
st.subheader("🗺️ 상위 5개 행정구역 위치 시각화")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_df,
    get_position='[lon, lat]',
    get_radius=10000,  # 반지름 (m)
    get_fill_color='[255, 0, 0, 100]',  # 빨간색, 투명도 100
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=map_df["lat"].mean(),
    longitude=map_df["lon"].mean(),
    zoom=6,
    pitch=0,
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# 표와 선그래프
st.subheader("📊 총인구수 기준 상위 5개 행정구역")
st.dataframe(top5_df[['행정구역', '총인구수']])

st.subheader("📈 연령별 인구 변화")

age_columns_only = top5_df.columns[2:-2]  # 'lat', 'lon' 제외

for _, row in top5_df.iterrows():
    st.write(f"### {row['행정구역']}")
    age_data = row[age_columns_only].astype(str).str.replace(',', '').astype(int)
    age_df = pd.DataFrame({
        '연령': age_columns_only,
        '인구수': age_data.values
    }).set_index('연령')
    st.line_chart(age_df)
