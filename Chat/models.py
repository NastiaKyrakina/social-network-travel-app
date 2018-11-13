from django.db import models
from django.contrib.auth.models import User


class ChatManager(models.Manager):

    def users_chats(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return

        chats = self.filter(member__user=user)
        return chats


class Chat(models.Model):

    name = models.CharField(max_length=25, blank=True)
    slug = models.SlugField(blank=True)
    date_create = models.DateField(auto_now_add=True)
    date_last_mess = models.DateTimeField(blank=True, null=True)
    members = models.ManyToManyField(User, through='Member')

    objects = models.Manager()
    chat_objects = ChatManager()

    def set_slug(self):
        self.slug = '%s_chat' % self.id

    def save(self, *args, **kwargs):
        self.set_slug()
        super(Chat, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def last_message(self):
        try:
            last_message = Message.objects.get(date=self.date_last_mess)
        except Message.DoesNotExist:
            return None
        return last_message

    def new_message(self, user_id):
        last_visit = self.member_set.get(user__id=1).last_visit
        new_message = self.objects.filter(message__date__gt=last_visit)
        return new_message


class Member(models.Model):
    user = models.ForeignKey(User, on_delete='Cascade')
    chat = models.ForeignKey(Chat, on_delete='Cascade')
    last_visit = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s | %s" % (self.user.username, self.chat.name)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete='Cascade')
    chat = models.ForeignKey(Chat, on_delete='Cascade')
    text = models.TextField(max_length=1000, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[0:100]

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        self.chat.date_last_mess = self.date
        self.chat.save()
