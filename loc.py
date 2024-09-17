import pandas as pd
from geopy.geocoders import Nominatim
df=pd.read_csv(r"C:\Users\janna\Desktop\me\healthcardloc.csv")
geolocator=Nominatim(user_agent="geoapiExercises")
def get_coordinates(location):
    try:
        location=geolocator.geocode(location)
        latitude=location.latitude
        longitude=location.longitude
        return latitude, longitude
    except:
        return None, None
df[['latitude', 'longitude']]=df['location'].apply(get_coordinates).tolist()
df.to_csv('loc.csv', index=False)
