import streamlit as st
import requests
import json
import folium
from streamlit_folium import folium_static

api_key = st.secrets["college_scorecard_api_key"]

# Set up Streamlit
st.title("🔍 College Explorer")
st.caption("✨ Please enter at least one search filter (school name, state, or zip code).")

# User inputs
school_name_col, state_col, zip_code_col = st.columns(3, gap="small")

school_name = school_name_col.text_input("School name")
state = state_col.text_input("State abbreviation (e.g. CA)")
zip_code = zip_code_col.text_input("Zip code")

if school_name or state or zip_code:
    # Build API request URL
    base_url = "https://api.data.gov/ed/collegescorecard/v1/schools.json"
    query_parameters = f"?api_key={api_key}&_fields=id,school.name,school.state,school.zip,school.city,location.lat,location.lon,latest.student.size"

    if school_name:
        query_parameters += f"&school.name={school_name}"
    if state:
        query_parameters += f"&school.state={state}"
    if zip_code:
        query_parameters += f"&zip={zip_code}"
    
    url = base_url + query_parameters

    # Fetch data from API
    response = requests.get(url)
    data = json.loads(response.text)

    if "results" in data:
        results = data["results"]
        st.info(f"Total results: {data['metadata']['total']}")

        latitudes = []
        longitudes = []
        for result in results:
            lat = result.get("location.lat", None)
            lon = result.get("location.lon", None)
            if lat and lon:
                latitudes.append(lat)
                longitudes.append(lon)

        # Calculate the average latitude and longitude
        avg_lat = sum(latitudes) / len(latitudes) if latitudes else 38.5
        avg_lon = sum(longitudes) / len(longitudes) if longitudes else -95

        # Create map centered at the average coordinates
        college_map = folium.Map(location=[avg_lat, avg_lon], zoom_start=7)

        for lat, lon, result in zip(latitudes, longitudes, results):
            folium.Marker(
                location=[lat, lon],
                popup=f"{result['school.name']} - {result['school.city']}, {result['school.state']}",
            ).add_to(college_map)

        folium_static(college_map)

        for result in results:
            st.markdown(
                f"**School Name:** {result['school.name']}<br>"
                f"**State:** {result['school.state']}<br>"
                f"**City:** {result['school.city']}<br>"
                f"**Zip Code:** {result['school.zip']}<br>"
                f"**Student Size:** {result.get('latest.student.size', 'N/A')}",
                unsafe_allow_html=True,
            )
            st.markdown("---")
    else:
        st.error("No results found or an error occurred. Please check your API key and filters.")
