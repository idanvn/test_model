import datetime
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

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
        location = {
            'city': data['city'],
            'region': data['region_name'],
            'country': data['country_name'],
            'latitude': data['latitude'],
            'longitude': data['longitude']
        }
    except requests.RequestException as e:
        print(f"Error fetching location data: {e}")
        location = {
            'city': 'Unknown',
            'region': 'Unknown',
            'country': 'Unknown',
            'latitude': None,
            'longitude': None
        }
    return location

def get_weather(latitude, longitude):
    """Get the current weather for the specified latitude and longitude using Open-Meteo API."""
    try:
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': True
        }
        response = requests.get('https://api.open-meteo.com/v1/forecast', params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        current_weather = data['current_weather']
        temperature = current_weather['temperature']
        weather = f"Temperature: {temperature}°C"
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        weather = "Weather data not available"
    return weather

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/status':
            current_date_time = get_current_date_time()
            location = get_location()
            if location['latitude'] and location['longitude']:
                weather = get_weather(location['latitude'], location['longitude'])
            else:
                weather = "Weather data not available"

            response_content = (
                "**********************************\n"
                "*        Current Status          *\n"
                "**********************************\n"
                f"* Location: {location['city']}, {location['region']}, {location['country']:<20} *\n"
                f"* Date and Time: {current_date_time:<14} *\n"
                f"* Weather: {weather:<28} *\n"
                "**********************************\n"
            )

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(response_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_server(port=2024):
    """Run the HTTP server on the specified port."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
