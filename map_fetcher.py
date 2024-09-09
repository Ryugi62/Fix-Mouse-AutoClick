# map_fetcher.py

import googlemaps
import requests
from PIL import Image
from io import BytesIO


def fetch_and_save_static_map(lat, lng, save_path):
    """
    Fetches a static satellite map image from Google Maps API and saves it to the specified path.

    :param api_key: Google Maps API key
    :param lat: Latitude of the location
    :param lng: Longitude of the location
    :param save_path: Path to save the satellite image
    """

    # .env 파일에서 API 키를 가져옴
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    gmaps = googlemaps.Client(key=api_key)
    static_map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=17&size=606x318&maptype=satellite&key={gmaps.key}"
    response = requests.get(static_map_url)
    if response.status_code == 200:
        try:
            image = Image.open(BytesIO(response.content))
            image.save(save_path)
            print(f"Image saved: {save_path}")
        except IOError:
            print("Unable to process the image file, it might be corrupted.")
    else:
        print(f"Failed to fetch the map image, status code: {response.status_code}")
