import csv
from geopy.geocoders import Nominatim

def add_lat_long_to_csv(csv_file):
    geolocator = Nominatim(user_agent="doctor-geocoding")
    updated_rows = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames + ['Latitude', 'Longitude']
        updated_rows.append(headers)

        for row in reader:
            address = row['Address']

            try:
                location = geolocator.geocode(address)

                if location is not None:
                    latitude = location.latitude
                    longitude = location.longitude
                else:
                    latitude = ''
                    longitude = ''

            except Exception as e:
                print(f"Error geocoding address: {address}. Skipping...")
                latitude = ''
                longitude = ''

            updated_rows.append(list(row.values()) + [latitude, longitude])

    with open('updated_' + csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    print(f"Latitude and longitude added to the CSV file: updated_{csv_file}")


# Provide the path to your CSV file
csv_file_path = 'output.csv'

# Call the function to add latitude and longitude columns to the CSV
add_lat_long_to_csv(csv_file_path)
