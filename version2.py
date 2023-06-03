import streamlit as st
import folium
from geopy.distance import geodesic
from streamlit_folium import folium_static
from ml import *


similar_text,final_df = get_similar_text_andDoctor_list()
# Assuming you already have the 'final_df' DataFrame

def create_map():
    # Create a map centered at Santa Clara University
    map_center = (37.349, -121.939)
    m = folium.Map(location=map_center, zoom_start=8)

    # Add Santa Clara University marker in red color
    santa_clara_marker = folium.Marker(
        location=(37.349, -121.939),
        popup='Santa Clara University',
        icon=folium.Icon(color='red', icon='university'),
    ).add_to(m)

    
    # Add clinic markers in blue color and connect with lines
    for i, row in final_df.iterrows():
        doctor_name = row['Doctor']
        doctor_speciality = row['Speciality']
        clinic_address = row['Address']
        clinic_distance = row['Distance(miles)']
        clinic_timings = row['Timings']
        clinic_insurance = row['Insurance']
        doctor_coordinates = (row['Latitude'], row['Longitude'])

        if pd.isnull(doctor_coordinates):
            st.write(f"Address with NaN location: {clinic_address}")
            continue

        # Create HTML for doctor name with clickable link
        doctor_name_link = f"<a href='{row['url']}' target='_blank'>{doctor_name}</a>"

        # Create HTML for clinic details
        clinic_details = f"{clinic_distance} miles<br>" \

        # Add clinic marker to the map
        folium.Marker(
            location=doctor_coordinates,
            popup=doctor_name_link + "<br>" + clinic_details,
            icon=folium.Icon(color='blue', icon='clinic-medical'),
        ).add_to(m)

        # Connect clinic marker with Santa Clara University
        folium.PolyLine(
            locations=[map_center, doctor_coordinates],
            color='blue',
            weight=1.5,
            opacity=1,
            tooltip=f"Distance: {clinic_distance} miles",
        ).add_to(m)

    return m

# Display the map in Streamlit
st.title('Doctor Map')
st.write('Map showing Santa Clara University and clinic locations')
map = create_map()
folium_static(map)

# Extract the list of doctors from 'final_df'
doctors_list = final_df['Doctor'].tolist()

# Display the list of doctors in Streamlit
st.title('List of Doctors')
for doctor in doctors_list:
    st.write(doctor)
    st.write('---')

# Highlight keywords from 'similar_text' in the doctor details
st.title('Highlighted Doctor Details')
for i, row in final_df.iterrows():
    doctor_name = row['Doctor']
    speciality = row['Speciality']
    highlighted_speciality = speciality

    for keyword in similar_text:
        if isinstance(highlighted_speciality, str):
            highlighted_speciality = highlighted_speciality.replace(keyword, f'<mark>{keyword}</mark>')

    st.write('Doctor:', doctor_name)
    st.write('Speciality:', highlighted_speciality)
    st.write('Address:', row['Address'])
    st.write('Distance (miles):', row['Distance(miles)'])
    st.write('Timings:', row['Timings'])
    st.write('Insurance:', row['Insurance'])
    st.write('---')

# Display the list of doctors in Streamlit
st.title('List of Doctors')
for doctor in doctors_list:
    speciality = doctor['Speciality']
    highlighted_speciality = speciality

    for keyword in similar_text:
        highlighted_speciality = highlighted_speciality.replace(keyword, f'<span style="font-weight:bold; color:red;">{keyword}</span>')

    st.write(f"<b>{doctor['Doctor']}</b>: {highlighted_speciality}", unsafe_allow_html=True)
    st.write('---')