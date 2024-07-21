import datetime
import requests

def get_current_date_time():
    """Get the current date and time as a formatted string."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def get_location():
    """Get the current location based on IP address."""
    try:
        response = requests.get('https://freegeoip.app/json/', timeout=5)
        response.raise_for_status()
        data = response.json()
        location = f"{data['city']}, {data['region_name']}, {data['country_name']}"
    except requests.RequestException:
        location = "Unknown Location"
    return location

def main():
    """Main function to print the current date, time, and location."""
    current_date_time = get_current_date_time()
    location = get_location()

    # Fancy output formatting
    print("**********************************")
    print("*        Current Status          *")
    print("**********************************")
    print(f"* Location: {location:<20} *")
    print(f"* Date and Time: {current_date_time:<14} *")
    print("**********************************")

if __name__ == "__main__":
    main()
