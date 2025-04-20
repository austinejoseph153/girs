from django.shortcuts import render
from django.views.generic.base import TemplateView
import folium
import json, requests
from geopy.geocoders import Nominatim
import folium.raster_layers
from .models import Location
from django.http import HttpResponseNotAllowed, JsonResponse
from .models import LocationCategory, Location
from .utils import get_location_info

# geolocator = Nominatim(user_agent="austine")
# location = geolocator.reverse("7.7288104,8.5535186")
# print(location.raw)

class HomeTemplateView(TemplateView):
    """
    Home
    """
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context["location_categories"] = LocationCategory.objects.all()
        return context

class MapTemplateView(TemplateView):
    
    template_name = "pages/map.html"

    def get_context_data(self, **kwargs):
        context = super(MapTemplateView, self).get_context_data(**kwargs)
        location = Location.objects.get(pk=self.request.GET.get("location_id"))
        start_coordinates = [7.73375000, 8.52139000]
        end_coordinates = [str(location.latitude), str(location.longitude)]
        user_latitude = self.request.GET.get("user_latitude", None)
        user_longitude = self.request.GET.get("user_longitude", None)
        # public_ip = requests.get("https://api.ipify.org")
        # public_ip = "10.250.228.80"
        # response = requests.get("http://ip-api.com/json").json()
        # print(response)
        # if user_latitude and user_longitude:
        # test_coordinates = [41.850030, -87.650050]
        m = folium.Map(
                        location=start_coordinates,
                        control_scale=True,
                        zoom_start=13,
                        height='100%',
                       )
        folium.FeatureGroup(name="Icon collection", control=False).add_to(m)

        # different kind of layers

        folium.Marker(location=start_coordinates, popup="Bsu markurdi" , icon=folium.Icon(color="red")).add_to(m)
        folium.Marker(location=end_coordinates, popup=location.name , icon=folium.Icon(color="green")).add_to(m)
        folium.PolyLine([start_coordinates, end_coordinates], color="blue").add_to(m)
        folium.LayerControl().add_to(m)

        # get info about the location
        location_info = get_location_info(location.latitude, location.longitude)
        context["location_info"] = location_info
        context["map"] = m._repr_html_()
        context["location"] =  location
        return context
    
def get_locations_by_category(request):
    category = request.GET.get("category")
    location_list = []
    locations = Location.objects.filter(category__name=category)
    if locations:
        for location in locations:
            data = {}
            data["name"] = location.name
            data["pk"] = location.pk
            # data["coordinates"] = "{} , {}".format(str(location.latitude), str(location.longitude)) 
            location_list.append(data)
    return JsonResponse({"locations":location_list})
