from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import *
from .models import *
from image_cropping import ImageCroppingMixin

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username",]

admin.site.register(CustomUser, CustomUserAdmin)

class ProfileModelAdmin(ImageCroppingMixin,admin.ModelAdmin):
    list_display = ["tmId","__str__","image", 'slug', 'timestamp', 'updated']
    list_display_links = ["__str__"]
    list_filter = ["gender","timestamp","dateOfBirth"]
    search_fields = ["name","countryOfOrigin","motherTongue"]

    class Meta:
        model = profiles

admin.site.register(profiles, ProfileModelAdmin)

