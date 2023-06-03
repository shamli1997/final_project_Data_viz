import streamlit as st
import folium
from streamlit_folium import folium_static
from data import doctors_data
from geopy.geocoders import Nominatim


# Santa Clara University coordinates
santa_clara_univ_coords = (37.349998, -121.938987)

# Create a Streamlit map component
st.title("Doctor's Clinic Map")

# Initialize the map centered at Santa Clara University
map_center = santa_clara_univ_coords
zoom_level = 13
map_obj = folium.Map(location=map_center, zoom_start=zoom_level)

# Create a geocoder using Nominatim
geolocator = Nominatim(user_agent="my-app")

# Add a marker for Santa Clara University (red color)
folium.Marker(location=santa_clara_univ_coords, popup="Santa Clara University", icon=folium.Icon(color="red")).add_to(map_obj)

# Iterate over each doctor's data
for doctor in doctors_data:
    # Geocode the clinic address
    clinic_address = doctor["address"]
    try:
        # Perform geocoding to get latitude and longitude coordinates
        location = geolocator.geocode(clinic_address)
        if location is not None:
            latitude, longitude = location.latitude, location.longitude

            # Add a marker for each clinic
            folium.Marker(location=[latitude, longitude], popup=f"<b>{doctor['name']}</b><br><a href='{doctor['link']}' target='_blank'>Doctor's Profile</a>").add_to(map_obj)

            # Draw a line between Santa Clara University and the clinic
            folium.PolyLine(
                locations=[santa_clara_univ_coords, (latitude, longitude)],
                color="blue",
                weight=2,
                opacity=1,
            ).add_to(map_obj)
    except Exception as e:
        st.warning(f"Geocoding failed for address: {clinic_address}. Error: {str(e)}")

# Display all clinic details
for clinic in doctors_data:
    st.write(f"Doctor: [{clinic['name']}]({clinic['link']})")
    st.write(f"Type: {clinic['specialty']}")
    st.write(f"Address: {clinic['address']}")
    st.write("---")

# Display the map using streamlit_folium
folium_static(map_obj)
