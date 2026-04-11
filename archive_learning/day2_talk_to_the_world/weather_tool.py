import requests

# STEP 1: GET COORDINATES FROM CITY NAME

def get_coordinates(city_name):
    """Convert city name to (latitude, longitude) using Open-Meteo Geocoding API."""

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json"
        }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() # Raise error if status != 200

        data = response.json()

        # city not found -> api returns empty list
        if not data.get("results"):
            return None

        city_data = data["results"][0] 
        return{
            "name": city_data["name"],
            "country": city_data.get("country", "Unknown"),
            "latitude": city_data["latitude"],
            "longitude": city_data["longitude"],
            "timezone": city_data.get("timezone", "UTC")
        }
    except requests.exceptions.ConnectionError:
        print(" NO INTERNET CONNECTION! Please check your connection and try again.")
        return None
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
        return None
             

# STEP 2: GET WEATHER USING COORDINATES

def get_weather(latitude, longitude, timezone):
    """Get current weather for given coordinates """

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": True,
        "timezone": timezone,
        "hourly": "relativehumidity_2m,apparent_temperature"
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"WEATHER FETCH FAILED: {e}")
        return None

# STEP 3: FROMAT AND PRINT WEATHER INFO

def interpret_weather_code(code):
    """ WMO weather codes: human readable"""
    weather_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        61: "slight rain",
        63: "moderate rain",
        71: "Slight snow",
        80: "Rain showers",
        95: "Thunderstorm"
    }
    return weather_map.get(code, f"CODE {code}")

def display_weather(city_info, weather_data):
    """ NICELY FORMAT AND PRINT WEATHER INFO"""
    current = weather_data["current_weather"]
    print("\n" + "🌍 " * 25)
    print(f"  📍 Location  : {city_info['name']}, {city_info['country']}")
    print(f"  🌡️  Temperature: {current['temperature']}°C")
    print(f"  💨 Wind Speed : {current['windspeed']} km/h")
    print(f"  🌬️  Wind Dir  : {current['winddirection']}°")
    print(f"  🌤️  Condition : {interpret_weather_code(current['weathercode'])}")
    print(f"  📅 Time       : {current['time']}")
    print(f"  🕐 Timezone   : {city_info['timezone']}")
    print("🌍 " * 25 + "\n")


# STEP 4: MAIN PROGRAM LOOP 

def main():
    print("\n" + "=" * 50)
    print("  🌤️  WEATHER TOOL  🌤️ 3000")
    print("=" * 50)
    
    while True:
        # Get user input
        city = input("\nEnter a city name (or 'exit' to quit): ").strip()

        if city.lower() == "quit":
            print("Goodbye!!")
            break
        if not city:
            print("Please enter a valid city name.")
            continue
        # Find City Coordinates
        print(f"\n LOOKING UP! '{city}'...")
        city_info = get_coordinates(city)

        if city_info is None:
            print(f"Sorry, couldn't find '{city}'.Check Spelling and Please try another city.")
            continue
        print(f" Found: {city_info['name']},{city_info['country']}")

        # Fetch Weather Data
        print(" FETCHING WEATHER DATA...")
        weather = get_weather(
            city_info["latitude"],
            city_info["longitude"],
            city_info["timezone"]
        )
        if weather is None:
            print(" COULD NOT FETCH WEATHER DATA. Please try again later.")
            continue
        # Display Weather Info
        display_weather(city_info, weather)
    
if __name__ == "__main__":
    main()
