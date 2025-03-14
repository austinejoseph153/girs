from django.contrib import admin
from .models import User

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Customer Info", {
            'fields': (
                ('firstname', 'lastname','email', 'phone', 'city', 'address', 'image'),
                ('password'),
            ),
        }),
    )

    list_display = ('id', 'firstname', 'lastname', 'email', 'phone',)

