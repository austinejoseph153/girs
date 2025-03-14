from django.urls import path
from .views import HomeTemplateView, MapTemplateView, get_locations_by_category


app_name = "pages"
urlpatterns = [
    path("", view=HomeTemplateView.as_view(), name="index"),
    path("map/", view=MapTemplateView.as_view(), name="map_page"),
    path("filter/locations/", view=get_locations_by_category, name="filter_locations")
]