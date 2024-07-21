import datetime
import requests

def get_current_date_time():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_location():
    try:
        response = requests.get("https://freegeoip.app/json/", timeout=5)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        data = response.json()
        location = {
            "IP Address": data.get("ip"),
            "City": data.get("city"),
            "Region": data.get("region_name"),
            "Country": data.get("country_name"),
            "Coordinates": f"{data.get('latitude')}, {data.get('longitude')}",
            "Organization": data.get("org"),
            "Timezone": data.get("time_zone")
        }
        return location
    except requests.RequestException as e:
        print(f"Error getting location from freegeoip.app: {e}")
        return None

if __name__ == "__main__":
    current_date_time = get_current_date_time()
    location = get_location()

    print(f"Current Date and Time: {current_date_time}")
    if location:
        print("Location Information:")
        for key, value in location.items():
            print(f"  {key}: {value}")
    else:
        print("Could not retrieve location.")
