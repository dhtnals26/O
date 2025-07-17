import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="연령별 인구 지도", layout="centered")

st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 불러오기
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 총인구수 숫자 처리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '', regex=False).astype(int)

# 연령별 컬럼 추출 및 이름 정리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
age_labels = []
for col in age_columns:
    if '100세 이상' in col:
        age_labels.append('100세 이상')
    else:
        age_labels.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + age_labels

# 총인구수 상위 5개 지역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 지도 표시용 위경도 정보 (예시 - 실제로는 더 확장 필요)
location_dict = {
    '서울특별시': [37.5665, 126.9780],
    '부산광역시': [35.1796, 129.0756],
    '인천광역시': [37.4563, 126.7052],
    '대구광역시': [35.8722, 128.6025],
    '대전광역시': [36.3504, 127.3845],
    '광주광역시': [35.1595, 126.8526],
    '울산광역시': [35.5384, 129.3114],
    '경기도 수원시': [37.2636, 127.0286]
}

# 위경도 컬럼 추가
top5_df["lat"] = top5_df["행정구역"].apply(lambda x: location_dict.get(x, [None, None])[0])
top5_df["lon"] = top5_df["행정구역"].apply(lambda x: location_dict.get(x, [None, None])[1])
map_df = top5_df.dropna(subset=["lat", "lon"])

# 지도 시각화
st.subheader("🗺️ 상위 5개 행정구역 위치 (지도 시각화)")

if not map_df.empty and map_df['lat'].notna().all() and map_df['lon'].notna().all():
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position='[lon, lat]',
        get_radius=15000,
        get_fill_color='[255, 0, 0, 120]',  # 반투명 빨간 원
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=map_df["lat"].mean(),
        longitude=map_df["lon"].mean(),
        zoom=6,
        pitch=0,
    )

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
else:
    st.warning("❌ 지도에 표시할 유효한 위치 정보가 없습니다.")

# 데이터 출력
st.subheader("📊 총인구수 기준 상위 5개 행정구역")
st.dataframe(top5_df[['행정구역', '총인구수']])

# 연령별 선 그래프
st.subheader("📈 상위 5개 행정구역의 연령별 인구 변화")

age_only_cols = top5_df.columns[2:-2]  # age만 선택 (lat, lon 제외)

for _, row in top5_df.iterrows():
    st.markdown(f"### 📍 {row['행정구역']}")
    age_data = row[age_only_cols].astype(str).str.replace(',', '', regex=False).astype(int)
    age_df = pd.DataFrame({
        '연령': age_only_cols,
        '인구수': age_data.values
    }).set_index('연령')
    st.line_chart(age_df)
