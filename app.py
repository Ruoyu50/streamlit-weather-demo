import streamlit as st
import requests

API_KEY = 'bc0dffe988a5874f093f027fbf71411f'

cities = [
    'New York', 'London', 'Paris', 'Tokyo', 'Los Angeles', 'Chicago', 'Toronto', 'Berlin', 'Madrid', 'Rome',
    'Sydney', 'Melbourne', 'Moscow', 'Dubai', 'Singapore', 'Seoul', 'Bangkok', 'Hong Kong', 'Buenos Aires',
    'Cape Town', 'Mexico City', 'Istanbul', 'Amsterdam', 'Vienna', 'Barcelona', 'Lisbon', 'Vancouver',
    'Cairo', 'Lagos', 'Mumbai'
]

st.title("Asking Weather App")

st.header("Check the weather by city")
city_input = st.text_input("How's the weather today? Enter city name:")

if st.button("Submit City"):
    if city_input:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city_input}&units=metric&appid={API_KEY}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            temp_f = (data['main']['temp'] * 9/5) + 32
            weather_desc = data['weather'][0]['description']
            st.success(f"{city_input} is {temp_f:.1f}°F, and {weather_desc}.")
        except Exception as e:
            st.error("City not found or API error.")
    else:
        st.warning("Please enter a city name.")

st.header("Find cities with specific temperature")
temp_input = st.number_input("What city is around what temperature today? (°F)", step=0.1, format="%.1f")

if st.button("Submit Temperature"):
    if temp_input is not None:
        matching_cities = []
        with st.spinner("Fetching data for cities..."):
            for city in cities:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
                try:
                    res = requests.get(url)
                    res.raise_for_status()
                    data = res.json()
                    temp_f = (data['main']['temp'] * 9/5) + 32
                    if abs(temp_f - temp_input) < 1.5:
                        matching_cities.append(city)
                except:
                    pass
        
        if matching_cities:
            shown_cities = matching_cities[:3]
            msg = f"{', '.join(shown_cities)} {'is' if len(shown_cities)==1 else 'are'} around {temp_input}°F today."
            if len(matching_cities) > 3:
                msg += f" (Showing 3 of {len(matching_cities)} matches)"
            st.success(msg)
        else:
            st.info("No cities match that temperature today.")
    else:
        st.warning("Please enter a temperature.")