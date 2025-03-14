from django.shortcuts import render
from django.views.generic.base import TemplateView
import folium
import json
from geopy.geocoders import Nominatim
import folium.raster_layers
from .models import Location
from django.http import HttpResponseNotAllowed, JsonResponse
from .models import LocationCategory, Location

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
        coordinates = [str(location.latitude), str(location.longitude)]
        # coordinates = [41.850030, -87.650050]
        m = folium.Map(
                        location=coordinates,
                        control_scale=True,
                        zoom_start=12,
                        height='100%',
                       )
        folium.FeatureGroup(name="Icon collection", control=False).add_to(m)

        # different kind of layers

        folium.Marker(location=coordinates, popup=location.name).add_to(m)
        folium.LayerControl().add_to(m)

        context["map"] = m._repr_html_()
        return context
    
    # def post(self, request, **kwargs): 
    #     context = {}
    #     return super(MapTemplateView, self).render_to_response(context)

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
