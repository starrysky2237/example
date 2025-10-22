import streamlit as st
import requests

# OpenWeatherMap API Key (⚠️ 실제 키로 변경해야 합니다!)
API_KEY = '6c40b0820856d83a30916a4ad306b932'

# 한글 도시명을 영어로 변환하는 매핑
CITY_MAPPING = {
    '서울': 'Seoul', '부산': 'Busan', '인천': 'Incheon', '대구': 'Daegu', '대전': 'Daejeon',
    '광주': 'Gwangju', '울산': 'Ulsan', '수원': 'Suwon', '창원': 'Changwon', '성남': 'Seongnam',
    '고양': 'Goyang', '용인': 'Yongin', '청주': 'Cheongju', '전주': 'Jeonju', '안산': 'Ansan',
    '천안': 'Cheonan', '제주': 'Jeju', '포항': 'Pohang', '강릉': 'Gangneung', '춘천': 'Chuncheon',
    '도쿄': 'Tokyo', '오사카': 'Osaka', '베이징': 'Beijing', '상하이': 'Shanghai',
    '뉴욕': 'New York', '런던': 'London', '파리': 'Paris', '로마': 'Rome',
}

def convert_city_name(input_city):
    """한글 도시명을 영어로 변환하고, 영문 도시명은 그대로 반환합니다."""
    city = input_city.strip()
    return CITY_MAPPING.get(city, city)

def recommend_clothing(temp):
    """기온에 따른 옷차림을 추천합니다."""
    if temp >= 28:
        return {"text": "민소매, 반팔, 반바지, 원피스", "emoji": "😎"}
    elif temp >= 23:
        return {"text": "반팔, 얇은 셔츠, 반바지, 면바지", "emoji": "👕"}
    elif temp >= 20:
        return {"text": "얇은 가디건, 긴팔, 면바지, 청바지", "emoji": "👚"}
    elif temp >= 17:
        return {"text": "얇은 니트, 맨투맨, 가디건, 청바지", "emoji": "🧶"}
    elif temp >= 12:
        return {"text": "자켓, 가디건, 야상, 스타킹, 청바지, 면바지", "emoji": "🧥"}
    elif temp >= 9:
        return {"text": "트렌치코트, 니트, 청바지, 스타킹, 따뜻한 옷", "emoji": "🧣"}
    elif temp >= 5:
        return {"text": "코트, 가죽자켓, 니트, 레깅스, 기모 바지", "emoji": "🧤"}
    else:
        return {"text": "패딩, 두꺼운 코트, 목도리, 기모제품, 방한용품", "emoji": "☃️"}

def get_weather_data(city_name):
    """OpenWeatherMap API에서 날씨 데이터를 가져옵니다."""
    converted_city = convert_city_name(city_name)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={converted_city}&appid={API_KEY}&units=metric&lang=kr"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # 4xx, 5xx 에러 발생 시 예외 처리
        data = response.json()
        
        # 날씨 데이터 추출
        temp = round(data['main']['temp'])
        weather_kr = data['weather'][0]['description']
        display_city_name = city_name.strip() if city_name.strip() in CITY_MAPPING else data['name']
        country = data['sys']['country']
        
        return {
            "temp": temp,
            "weather_kr": weather_kr,
            "display_city_name": display_city_name,
            "country": country
        }
    except requests.exceptions.RequestException as e:
        st.error(f"❌ 날씨 정보를 가져오는 중 오류가 발생했습니다: {e}")
        return None
    except KeyError:
        st.error(f"❌ 도시 **{city_name}**의 날씨 정보를 찾을 수 없습니다. 도시 이름을 다시 확인해주세요.")
        return None

# ==============================================================================
# Streamlit UI 구성
# ==============================================================================

# 페이지 설정
st.set_page_config(
    page_title="날씨 & 옷차림 추천",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Streamlit의 Markdown과 HTML을 활용하여 CSS 없이 디자인 요소 구현
st.markdown("""
    <style>
    /* 전체 배경 그라데이션 (Streamlit의 body와 유사하게) */
    .stApp {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        min-height: 100vh;
    }
    /* 컨테이너처럼 보이게 중앙 영역의 배경과 패딩 설정 */
    .block-container {
        max-width: 500px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* 제목 스타일 */
    h1 {
        text-align: center;
        /* 웹 색상 대신 Streamlit의 텍스트 색상 사용 */
        color: #1d4ed8; 
        font-weight: 800;
        margin-bottom: 1.5rem;
    }
    /* 온도 표시 (크게 강조) */
    .temperature-display {
        text-align: center;
        font-size: 72px;
        font-weight: 900;
        color: #4facfe; /* 밝은 파랑 */
        margin: 10px 0 20px 0;
    }
    /* 추천 옷차림 섹션 스타일 */
    .recommendation-box {
        background-color: #e0f2fe; /* 매우 밝은 파랑 배경 */
        border: 3px solid #60a5fa; /* 파란색 테두리 */
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin-top: 30px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    .clothing-emoji {
        font-size: 64px;
        margin: 10px 0 15px 0;
    }
    .clothing-text {
        font-size: 18px;
        font-weight: 600;
        color: #0f172a;
        line-height: 1.8;
    }
    .section-title {
        color: #1d4ed8;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 10px;
    }
    .weather-info {
        color: #64748b;
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌤️ 오늘의 날씨 & 옷차림 추천")

# 1. 입력 섹션
# Streamlit은 사용자 정의 라디오 버튼을 지원하지 않으므로, 텍스트 입력만 사용합니다.
# "현재 위치" 기능은 Streamlit에서 복잡하므로 "도시 직접 입력"만 구현합니다.

city_input = st.text_input(
    "🔍 **도시 이름을 입력하세요** (예: 서울, 부산, Tokyo)", 
    value="서울",
    placeholder="도시 이름 입력",
    key="city_input_key"
)

st.caption("✨ 한글과 영어 모두 지원합니다.")

# 2. 날씨 확인 버튼
if st.button("🌤️ 날씨 확인하기", use_container_width=True):
    if not city_input:
        st.error("도시 이름을 입력해주세요.")
    else:
        # 날씨 데이터 가져오기
        with st.spinner('날씨 정보를 불러오는 중...'):
            weather_data = get_weather_data(city_input)

        if weather_data:
            temp = weather_data['temp']
            clothing = recommend_clothing(temp)
            
            # 3. 결과 표시
            st.markdown(f"""
                <div style="text-align: center; margin-top: 35px;">
                    <div style="font-size: 26px; font-weight: 700; color: #1e293b; margin-bottom: 10px;">
                        📍 {weather_data['display_city_name']} ({weather_data['country']})
                    </div>
                    
                    <div class="temperature-display">{temp}°C</div>
                    
                    <div class="weather-info">
                        {weather_data['weather_kr']}
                    </div>
                    
                    <div class="recommendation-box">
                        <div class="clothing-emoji">{clothing['emoji']}</div>
                        <div class="section-title">👔 오늘의 추천 옷차림</div>
                        <p class="clothing-text">{clothing['text']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# 페이지 로드 시 기본값으로 '서울'의 날씨를 표시 (선택 사항)
if 'init_load' not in st.session_state:
    st.session_state.init_load = True
    # 초기 로드 시 자동으로 날씨 정보를 표시하려면 아래 코드를 활성화하세요.
    # st.session_state.city_input_key = "서울"
    # st.experimental_rerun()