from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="doctor-geocoding")
address = '456 Elm St, Santa Clara, CA 95051'
location = geolocator.geocode(address)
print(location.latitude)
print(location.longitude)