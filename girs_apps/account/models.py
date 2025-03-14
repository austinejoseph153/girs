from django.db import models
from django.utils.translation import gettext_lazy as _

class User(models.Model):
    firstname = models.CharField(max_length=100, verbose_name=_("First Name"))
    lastname = models.CharField(max_length=100, verbose_name=_("Last Name"))
    email = models.EmailField(max_length=100, verbose_name=_("Email"))
    password = models.CharField(max_length=100, verbose_name=_("Password"))
    phone = models.CharField(max_length=100, verbose_name=_("Phone"))
    city = models.CharField(max_length=100, verbose_name=_("City"))
    address = models.CharField(max_length=100, verbose_name=_("Address"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    image = models.ImageField(upload_to="user_images/", verbose_name=_("Image"), null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.firstname, self.lastname)
    
    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
