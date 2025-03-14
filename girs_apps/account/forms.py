from django import forms
from django.utils.translation import gettext_lazy as _

class UserForm(forms.Form):
    firstname = forms.CharField(max_length=100, label=_("First Name"), widget=forms.TextInput(attrs={"class": "form-control"}))
    lastname = forms.CharField(max_length=100, label=_("Last Name"), widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=100, label=_("Email"), widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=100, label=_("Password"), widget=forms.PasswordInput(attrs={"class": "form-control"}))
    phone = forms.CharField(max_length=100, label=_("Phone"), widget=forms.TextInput(attrs={"class": "form-control"}))
    city = forms.CharField(max_length=100, label=_("City"), widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(max_length=100, label=_("Address"), widget=forms.TextInput(attrs={"class": "form-control"}))
    image = forms.ImageField(label=_("Image"), widget=forms.FileInput(attrs={"class": ""}), required=False)

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100, label=_("Email"), widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=100, label=_("Password"), widget=forms.PasswordInput(attrs={"class": "form-control"}))