# 지도용 데이터프레임 만들기
top5_df["lat"] = top5_df["행정구역"].apply(lambda x: location_dict.get(x, [None, None])[0])
top5_df["lon"] = top5_df["행정구역"].apply(lambda x: location_dict.get(x, [None, None])[1])
map_df = top5_df.dropna(subset=["lat", "lon"])

# 지도 시각화
st.subheader("🗺️ 상위 5개 행정구역 위치")

if not map_df.empty and map_df['lat'].notna().all() and map_df['lon'].notna().all():
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position='[lon, lat]',
        get_radius=10000,
        get_fill_color='[255, 0, 0, 100]',
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=map_df["lat"].mean(),
        longitude=map_df["lon"].mean(),
        zoom=6
    )

    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
else:
    st.warning("❌ 지도에 표시할 유효한 위치 정보가 없습니다.")
