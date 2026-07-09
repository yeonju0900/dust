@st.cache_data
def load_data():
    file_name = "dustdata.csv" # 깃허브에 올리신 파일명과 정확히 일치해야 합니다.
    
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
