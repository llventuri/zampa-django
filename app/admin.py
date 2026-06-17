from django.contrib import admin
from app.models import DogProfile,Profile,BoardPost
# Register your models here.

admin.site.register([DogProfile,Profile,BoardPost])