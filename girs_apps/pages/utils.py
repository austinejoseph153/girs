from geopy.geocoders import Nominatim

def get_location_info(lat, lon):
    geolocator = Nominatim(user_agent="my_user_agent")
    location = geolocator.reverse(f"{lat}, {lon}")
    location =  location.raw
    location_info = {
        "display Name": location.get("display_name"),
        "Country": location.get("address").get("country"),
        "State": location.get("address").get("state"),
        "City": location.get("address").get("city"),
        "Latitude": location.get("lat"),
        "Longitude": location.get("lon"),
        "Type": location.get("type"),
        "Address Type": location.get("address_type"),
        "Class": location.get("class")
    }
    return location_info