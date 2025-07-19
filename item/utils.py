import requests

def reverse_geocode(lat,lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': float(lat),
            'lon': float(lon),
            'format': 'json',
            'accept-language': 'en',
        }
        headers = {
            'User-Agent': 'LostAndFound/1.0'
        }

        response = requests.get(url, params=params, headers=headers,timeout=5)

        if response.status_code == 200:
            return response.json().get('display_name')
    except Exception as e:
        return None

