import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 기본 설정
st.set_page_config(page_title="서울시 미세먼지 대시보드", page_icon="☁️", layout="wide")

# 2. 데이터 불러오기 (캐싱을 통해 앱 속도 향상)
@st.cache_data
def load_data():
    file_name = "dust.csv" # 깃허브에 올리신 파일명과 정확히 일치해야 합니다.
    
    try:
        # 1. 한국어 윈도우/엑셀 기본 인코딩인 cp949로 시도
        df = pd.read_csv(file_name, encoding="cp949")
    except UnicodeDecodeError:
        try:
            # 2. 실패 시 utf-8-sig (BOM이 포함된 UTF-8)로 시도
            df = pd.read_csv(file_name, encoding="utf-8-sig")
        except UnicodeDecodeError:
            # 3. 그래도 실패하면 euc-kr로 시도
            df = pd.read_csv(file_name, encoding="euc-kr")
            
    # '일시' 컬럼을 날짜/시간 타입으로 변환
    df['일시'] = pd.to_datetime(df['일시'])
    
    # 데이터 강제 숫자 변환 (결측치는 NaN 처리)
    df['미세먼지(PM10)'] = pd.to_numeric(df['미세먼지(PM10)'], errors='coerce')
    df['초미세먼지(PM25)'] = pd.to_numeric(df['초미세먼지(PM25)'], errors='coerce')
    
    return df

df = load_data()

# 3. 사이드바(Sidebar) 검색 필터 구현
st.sidebar.header("🔍 검색 설정")

# '구분' 컬럼에서 고유한 구 이름 목록 추출 (가나다 순 정렬)
gu_list = df['구분'].dropna().unique().tolist()
gu_list.sort()

# 드롭다운으로 구 선택
selected_gu = st.sidebar.selectbox("자치구를 선택하세요:", gu_list)

# 선택된 구의 데이터만 필터링 후 시간순 정렬
filtered_df = df[df['구분'] == selected_gu].sort_values('일시')

# 4. 메인 화면 구성
st.title("☁️ 2025년 서울시 (초)미세먼지 대시보드")
st.markdown(f"**{selected_gu}**의 시간별 미세먼지 및 초미세먼지 변화를 확인하세요.")

# 평균값 요약 정보 보여주기
col1, col2 = st.columns(2)
with col1:
    avg_pm10 = filtered_df['미세먼지(PM10)'].mean()
    st.metric(label="연간 평균 미세먼지(PM10)", value=f"{avg_pm10:.1f} ㎍/㎥")
with col2:
    avg_pm25 = filtered_df['초미세먼지(PM25)'].mean()
    st.metric(label="연간 평균 초미세먼지(PM25)", value=f"{avg_pm25:.1f} ㎍/㎥")

st.divider()

# 5. Plotly를 이용한 인터랙티브 시계열 그래프
fig = px.line(
    filtered_df, 
    x='일시', 
    y=['미세먼지(PM10)', '초미세먼지(PM25)'],
    labels={'value': '농도 (㎍/㎥)', 'variable': '측정 항목', '일시': '시간'},
    color_discrete_map={'미세먼지(PM10)': '#1f77b4', '초미세먼지(PM25)': '#ff7f0e'}
)

# 그래프 레이아웃 다듬기
fig.update_layout(
    xaxis_title="날짜 및 시간",
    yaxis_title="농도 (㎍/㎥)",
    legend_title_text="항목",
    hovermode="x unified"
)

# 스트림릿에 그래프 출력
st.plotly_chart(fig, use_container_width=True)

# 6. 상세 데이터 표 확인 기능 (토글)
if st.sidebar.checkbox("상세 데이터 표 보기"):
    st.subheader(f"📋 {selected_gu} 상세 데이터")
    st.dataframe(filtered_df.reset_index(drop=True))
