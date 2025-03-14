from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import FormView
import datetime
import uuid
from pathlib import Path
import os
import json
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginForm, UserForm
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext_lazy as _
from .models import User
from girs_apps.pages.models import Location, LocationCategory
from django.http import HttpResponseNotAllowed, HttpResponse, Http404, JsonResponse
from .auth import user_authenticate, user_login, user_logout, user_is_authenticated

class LoginRegisterTemplateView(TemplateView):
    template_name = "account/login_register.html"

    def render_to_response(self, context, **kwargs):
        response = super(LoginRegisterTemplateView, self).render_to_response(context, **kwargs)
        return response
    
    def get_context_data(self, **kwargs):
        context = super(LoginRegisterTemplateView, self).get_context_data(**kwargs)
        context["login_form"] = LoginForm()
        context["user_form"] = UserForm()
        return context
    
    def post(self, request, **kwargs): 
        context = {}
        action = request.POST.get("action")
        if action == "login":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = user_authenticate(request, login_form.cleaned_data['email'], login_form.cleaned_data['password'])
                if user:
                    user_login(request, user)
                    messages.success(request, _("Login successful"))
                    return redirect("account:user_dashboard")
                else:
                    context["login_form"] = login_form
                    context["user_form"] = UserForm()
                    messages.error(request,_("Invalid Email or password!"))
                    return super(LoginRegisterTemplateView, self).render_to_response(context)    
            else:
                context["login_form"] = login_form
                context["user_form"] = UserForm()
                messages.error(request,_("Invalid Email or password!"))
                return super(LoginRegisterTemplateView, self).render_to_response(context)
        else:
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                if User.objects.filter(email=user_form.cleaned_data["email"]).exists():
                    messages.error(request,_("user with email already exist"))
                    context["user_form"] = user_form
                    context["login_form"] = LoginForm()
                else:
                    user = User(**user_form.cleaned_data)
                    image_file = request.FILES.get("image")
                    user.image = image_file
                    user.save()
                    context["user_form"] = UserForm()
                    context["login_form"] = LoginForm()
                    messages.success(request, _("Account created successfully"))
                return super(LoginRegisterTemplateView, self).render_to_response(context)
            else:
                context["user_form"] = user_form
                context["login_form"] = LoginForm()
                messages.error(request, _("invalid form data"))
                return super(LoginRegisterTemplateView, self).render_to_response(context)

def check_if_user_is_authenticated(request):
    user = user_is_authenticated(request)
    if user:
        image_url = None
        if user.image:
            image_url = user.image.url
        return JsonResponse({"is_authenticated": True, "name": user.firstname,"image_url":image_url})
    else:
        return JsonResponse({"is_authenticated": False})

def user_logout_view(request):
    """
    Logout
    """
    user_logout(request)
    return redirect('pages:index')


def user_dashboard(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        context["user"] = user
        context["user_listings"] = Location.objects.filter(user=user).count()
        return render(request, "account/dashboard/index.html", context=context)
    else:
        return redirect("account:login_register")
    

def user_profile(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        context["user"] = user
        return render(request, "account/dashboard/profile.html",context=context)
    else:
        return redirect("account:login_register")

def change_password(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        context["user"] = user
        if request.method == "POST":
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")
            if user.password == old_password:
                if new_password == confirm_password:
                    user.password = new_password
                    user.save()
                    messages.success(request, _("Password changed successfully"))
                    return redirect("account:user_profile")
                else:
                    messages.error(request, _("New password and confirm password does not match"))
                    return render(request, "account/dashboard/change_password.html", context=context)
            else:
                messages.error(request, _("Old password is incorrect"))
                return render(request, "account/dashboard/change_password.html", context=context)
        else:
            return render(request, "account/dashboard/change_password.html", context=context)
    else:
        return redirect("account:login_register")
    
def add_listings(request):
    user = user_is_authenticated(request)
    if user:
        location_categories = LocationCategory.objects.all()
        context = {}
        context["user"] = user
        context["location_categories"] = location_categories
        if request.method == "POST":
            location_name = request.POST.get("location_name")
            location_description = request.POST.get("location_description")
            location_category = request.POST.get("location_category")
            latitude = request.POST.get("latitude")
            longitude = request.POST.get("longitude")
            image = request.FILES.get("image")
            location = Location(
                name=location_name, 
                description=location_description, 
                category_id=location_category, 
                latitude=latitude,
                user=user, 
                longitude=longitude, 
                image=image)
            location.save()
            messages.success(request, _("Location added successfully"))
            return redirect("account:my_listings")
        else:
            return render(request, "account/dashboard/add_listings.html", context=context)
    else:
        return redirect("account:login_register")
    
def delete_listing(request, id):
    user = user_is_authenticated(request)
    if user:
        location = Location.objects.get(pk=id)
        if location.user != user:
            location.delete()
            messages.success(request, _("Location deleted successfully"))
            return redirect("account:my_listings")
        else:
            messages.warning(request, _("You do not have permission to perform this operation"))
            return redirect("account:my_listings")
    else:
        return redirect("account:login_register")

def my_listings(request):
    user = user_is_authenticated(request)
    if user:
        context = {}
        locations = Location.objects.filter(user=user)
        context["user"] = user
        context["locations"] = locations
        return render(request, "account/dashboard/listings.html", context=context)
    else:
        return redirect("account:login_register")