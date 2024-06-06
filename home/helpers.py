from datetime import datetime
import requests

def convet_date(date_str):
    try:
        # Parse the date string
        parsed_date = datetime.strptime(date_str, "%B %d, %Y")

        # Format the date as YYYY-MM-DD
        formatted_date = parsed_date.strftime("%Y-%m-%d")
        return formatted_date
        print("Original Date:", date_str)
        print("Formatted Date:", formatted_date)
    except ValueError as e:
        print("Error:", e)


def get_geo_location(latitude,longitude):
    print(latitude,latitude)
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={longitude},{latitude}&key=AIzaSyDRrh9wAhF0e0iMc3a6LrfmdI2Z_CFGZ1A"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data)
        if 'results' in data and len(data['results']) > 0:
            city = None
            admin_area_2 = None
            admin_area_1 = None
            
            for result in data['results']:
                for component in result['address_components']:
                    if 'locality' in component['types']:
                        city = component['long_name']
                    elif 'administrative_area_level_2' in component['types']:
                        admin_area_2 = component['long_name']
                    elif 'administrative_area_level_1' in component['types']:
                        admin_area_1 = component['long_name']
            
            if city:
                return city
            elif admin_area_2:
                return admin_area_2
            elif admin_area_1:
                return admin_area_1
            else:
                return "No city or administrative area found in the address components."
        else:
            return "No address found for the given coordinates."
    else:
        return f"Error: {response.status_code}"
    return "Patna"