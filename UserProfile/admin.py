from django.contrib import admin

from HouseSearch.models import House, HousePhoto, Rate
from . import models


# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Note)
admin.site.register(models.Attachment)
admin.site.register(models.Country)
admin.site.register(House)
admin.site.register(HousePhoto)
admin.site.register(Rate)
