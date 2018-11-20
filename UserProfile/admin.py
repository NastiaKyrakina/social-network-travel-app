from django.contrib import admin

from HouseSearch.models import House, HousePhoto, Rate
from Chat.models import Chat, Message, Member
from . import models


# Register your models here.

admin.site.register(models.UserInfo)
admin.site.register(models.Note)
admin.site.register(models.Attachment)
admin.site.register(models.Country)
admin.site.register(House)
admin.site.register(HousePhoto)
admin.site.register(Rate)

admin.site.register(Chat)
admin.site.register(Member)
admin.site.register(Message)

admin.site.register(models.Diary)
admin.site.register(models.Marker)
