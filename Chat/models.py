from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):

    name = models.CharField(max_length=25, blank=True)
    slug = models.SlugField(blank=True)
    date_create = models.DateField(auto_now_add=True)

    def set_slug(self):
        self.slug = '%s-chat' % self.id


class Member(models.Model):
    user = models.ForeignKey(User, on_delete='Cascade')
    chat = models.ForeignKey(Chat, on_delete='Cascade')
    last_visit = models.DateTimeField(auto_now=True)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete='Cascade')
    chat = models.ForeignKey(Chat, on_delete='Cascade')
    text = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)
