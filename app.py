import streamlit as st
import folium
from geopy.distance import geodesic
from data import doctors_data
from streamlit_folium import folium_static
from ml import *

similar_text,final_df = get_similar_text_andDoctor_list()


def create_map():
    # Create a map centered at Santa Clara University
    map_center = (37.349, -121.939)
    m = folium.Map(location=map_center, zoom_start=8)

    # Add Santa Clara University marker with two icons
    santa_clara_marker = folium.Marker(
        location=(37.349, -121.939),
        popup='Santa Clara University',
        icon=folium.Icon(color='red', icon='university'),
    )
    santa_clara_marker.add_child(folium.Icon(color='red', icon='star'))
    santa_clara_marker.add_to(m)

    # Add clinic markers in blue color and connect with lines
    for i,doctor in final_df.iterrows():
        # Create HTML for doctor name with clickable link
        doctor_name = f"<a href='{doctor['url']}' target='_blank' style='text-decoration: underline; color: #333; font-weight: bold;'>{doctor['Doctor']}</a>"

        clinic_marker = folium.Marker(
            location=(doctor['Latitude'], doctor['Longitude']),
            popup=doctor_name,
            icon=folium.Icon(color='blue', icon='clinic-medical', prefix='fa'),
        ).add_to(m)

        distance = calculate_distance(map_center, (doctor['Latitude'], doctor['Longitude']))

        folium.PolyLine(
            locations=[map_center, (doctor['Latitude'], doctor['Longitude'])],
            color='blue',
            weight=1.5,
            opacity=1,
            tooltip=f"Distance: {distance} miles",
        ).add_to(m)

    return m

def calculate_distance(point1, point2):
    # Calculate distance between two points in miles using geodesic distance
    return round(geodesic(point1, point2).miles, 2)



# Display the list of doctors in Streamlit
st.title('List of Doctors')
for i, row in final_df.iterrows():
    doctor_name = row['Doctor']
    speciality = row['Speciality']
    clinic_distance = row['Distance(miles)']

    # Convert the list of specialities to a string
    speciality_str = ', '.join(speciality)
    # Remove the square brackets and single quotes
    # speciality_str = speciality_str.replace("[", "").replace("]", "").replace("'", "")

    
    # Highlight keywords in the speciality
    for keyword in similar_text:
        print(keyword)
        if keyword in speciality_str:
            print("IT IS PRESENT")
        speciality_str = speciality_str.replace(keyword, f"**<span style='background-color: lightgreen;'>{keyword}</span>**")
    
    print("============speciality_str=====",speciality_str)
    # Display the doctor's details
    st.markdown(f"**{doctor_name}**")
    st.markdown(f"**Speciality:** {speciality_str}", unsafe_allow_html=True)
    st.write('**Distance (miles):**', clinic_distance)
    st.write('---')




# Display the map in Streamlit
st.title('Doctor Map')
st.write('Map showing Santa Clara University and clinic locations')

map = create_map()
folium_static(map)
