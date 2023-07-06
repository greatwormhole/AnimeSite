from django.contrib import admin
from django.apps import apps
from .models import *

admin.site.register(Manga)
admin.site.register(Anime)
admin.site.register(Profile)

main_models = apps.get_app_config('main').get_models()

for model in main_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
