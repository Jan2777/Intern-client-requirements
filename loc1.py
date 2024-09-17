import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
def geocode_location(location):
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location_data = geolocator.geocode(location, timeout=10)
        if location_data:
            return location_data.latitude, location_data.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None
df = pd.read_csv(r"C:\Users\janna\Desktop\me\loc.csv")

for index, row in df.iterrows():
    if pd.isnull(row['latitude']) or pd.isnull(row['longitude']):
        location=row['location']
        latitude,longitude=geocode_location(location)
        if latitude and longitude:
            df.at[index, 'latitude'] = latitude
            df.at[index, 'longitude'] = longitude
df.to_csv(r"C:\Users\janna\Desktop\me\loc.csv", index=False)
