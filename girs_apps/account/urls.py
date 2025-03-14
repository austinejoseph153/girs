from django.urls import path
from .views import (
    LoginRegisterTemplateView, user_dashboard,
    user_logout_view, check_if_user_is_authenticated, 
    user_profile, change_password, my_listings, add_listings, delete_listing
)

app_name = "account"
urlpatterns = [
    path("login-register/", view=LoginRegisterTemplateView.as_view(), name="login_register"),
    path("user-dashboard/", view=user_dashboard, name="user_dashboard"),
    path("user-profile/", view=user_profile, name="user_profile"),
    path("user-is-authenticated/", view=check_if_user_is_authenticated, name="user_is_authenticated"),
    path("change/user/password/", view=change_password, name="change_password"),
    path("listings/", view=my_listings, name="my_listings"),
    path("add/listings/", view=add_listings, name="add_listings"),
    path("delete/listing/<int:id>/", view=delete_listing, name="delete_listing"),
    path("logout/", view=user_logout_view, name="user_logout"),
]