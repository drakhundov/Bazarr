from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="Bazarr")


def get(latitude, longitude):
    """Obtains country and area within a country which latitude and longitude specified correspond to."""
    g = geolocator.reverse(f"{latitude}, {longitude}", language="en").raw
    return g["address"]["ISO3166-2-lvl4"]
