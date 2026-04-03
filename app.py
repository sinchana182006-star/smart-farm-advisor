import streamlit as st
import requests
import pickle
from streamlit_mic_recorder import mic_recorder

# -------------------------------
# API KEY
# -------------------------------
API_KEY = "8bec7150cc52ab5eafc832ddbfd6a5da"

# -------------------------------
# Load model
# -------------------------------
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    st.error("❌ model.pkl not found")
    st.stop()

# -------------------------------
# Weather function
# -------------------------------
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        data = requests.get(url).json()

        if data.get("cod") != 200:
            return None, None

        return data["main"]["temp"], data["main"]["humidity"]
    except:
        return None, None

# -------------------------------
# UI
# -------------------------------
st.set_page_config(page_title="Smart Farm Advisor", layout="wide")
st.title("🌱 Smart Farm Advisor")

# -------------------------------
# 🎤 Voice Input (SAFE VERSION)
# -------------------------------
st.write("🎤 Voice Input (optional)")

audio = mic_recorder(
    start_prompt="🎙 Start",
    stop_prompt="⏹ Stop",
    just_once=True
)

if audio:
    st.success("✅ Voice recorded!")

    # NOTE: We don't convert to text (unstable)
    st.info("👉 Voice recorded. Please type city below.")

# -------------------------------
# City input (MAIN)
# -------------------------------
city = st.text_input("📍 Enter your city or village")

temp, humidity = None, None

if city:
    temp, humidity = get_weather(city)

    if temp is not None:
        st.success(f"🌡 Temp: {temp}°C | 💧 Humidity: {humidity}%")
    else:
        st.error("❌ Location not found (try nearest city)")

# -------------------------------
# Session state
# -------------------------------
if "N" not in st.session_state:
    st.session_state.N = 0.0
    st.session_state.P = 0.0
    st.session_state.K = 0.0
    st.session_state.ph = 0.0
    st.session_state.rainfall = 0.0

# -------------------------------
# Auto Fill
# -------------------------------
if st.button("⚡ Auto Fill Data"):
    st.session_state.N = 50
    st.session_state.P = 40
    st.session_state.K = 40
    st.session_state.ph = 6.5
    st.session_state.rainfall = 200

# -------------------------------
# Soil Inputs
# -------------------------------
st.subheader("🌾 Soil Details")

col1, col2 = st.columns(2)

with col1:
    st.number_input("Nitrogen", key="N")
    st.number_input("Phosphorus", key="P")
    st.number_input("Potassium", key="K")

with col2:
    st.number_input("pH", key="ph")
    st.number_input("Rainfall", key="rainfall")

# -------------------------------
# Predict
# -------------------------------
if st.button("🌱 Predict Crop"):
    if temp is None:
        st.error("❌ Enter valid location first")
    else:
        result = model.predict([[ 
            st.session_state.N,
            st.session_state.P,
            st.session_state.K,
            temp,
            humidity,
            st.session_state.ph,
            st.session_state.rainfall
        ]])

        st.success(f"🌾 Recommended Crop: {result[0]}")