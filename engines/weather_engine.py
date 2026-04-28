import requests

API_KEY = "b2cf7ced19646e4c825197e97e20bef7"


def get_weather(city):
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )

        res = requests.get(url, timeout=5)
        data = res.json()

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        # rainfall may not always exist
        rainfall = 50

        if "rain" in data:
            rainfall = data["rain"].get("1h", 50)

        return {
            "temperature": temp,
            "humidity": humidity,
            "rainfall": rainfall
        }

    except Exception as e:
        print("Weather Error:", e)

        return None