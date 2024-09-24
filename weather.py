import streamlit as st
import requests
import openai

# Function to get weather information
def get_weather(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    return response.json()

def generate_response(weather_info):
    prompt = (
        f"The current weather in {weather_info['name']} is as follows:\n"
        f"Temperature: {weather_info['main']['temp']}°C\n"
        f"Weather: {weather_info['weather'][0]['description']}\n"
        f"Humidity: {weather_info['main']['humidity']}%\n"
        f"Wind Speed: {weather_info['wind']['speed']} m/s\n\n"
        "Provide a summary of today's weather in this city."
    )
    openai_response = openai.chat.completions.create(
        model='gpt-3.5-turbo',
    
        messages=[{'role': 'user', 'content': prompt}]
    )
    return openai_response.choices[0].message.content

# Streamlit App
def main():
    st.title('Weather and Summary App')

    # API keys (You can also load these from environment variables or a secure vault)
    weather_api_key = "..........."  # Replace with your actual OpenWeatherMap API key
    openai.api_key = "...................................."  # Replace with your actual OpenAI API key

    city = st.text_input('Enter city name', 'New York')

    if st.button('Get Weather'):
        if city:
            weather_info = get_weather(city, weather_api_key)

            if weather_info.get("cod") != 200:
                st.error(f"Failed to get weather data: {weather_info.get('message', 'Unknown error')}")
            else:
                st.write(f"**City:** {weather_info['name']}")
                st.write(f"**Temperature:** {weather_info['main']['temp']}°C")
                st.write(f"**Weather:** {weather_info['weather'][0]['description']}")
                st.write(f"**Humidity:** {weather_info['main']['humidity']}%")
                st.write(f"**Wind Speed:** {weather_info['wind']['speed']} m/s")

                summary = generate_response(weather_info)
                st.write(f"**Summary:** {summary}")

if __name__ == "__main__":
    main()



