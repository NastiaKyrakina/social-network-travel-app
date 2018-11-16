from django.db import models
from django.contrib.auth.models import User
from Lib import FFD


class ChatManager(models.Manager):

    def users_chats(self, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return

        chats = self.filter(member__user=user)
        return chats


class MessageManager(models.Manager):

    def last_10_messages(self, chat, since=None):
        qs = self.filter(chat=chat).order_by('-date')
        if since:
            qs = qs.filter(date__lte=since)
        qs = qs[0:10]
        return qs


class Chat(models.Model):
    P2P = 0
    PRIVATE = 1
    PUBLIC = 2

    TYPE_CHATS = (
        (P2P, 'Talk'),
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
    )

    name = models.CharField(max_length=25, blank=True)
    slug = models.SlugField(blank=True)
    chat_type = models.SmallIntegerField(choices=TYPE_CHATS, default=P2P)
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

    def members(self):
        return self.member_set.all()


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

    message_object = MessageManager()
    objects = models.Manager()

    def __str__(self):
        return self.text[0:100]

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
        self.chat.date_last_mess = self.date
        self.chat.save()

    def has_files(self):
        return self.messageattachment_set.all()

    def get_images(self):
        return self.messageattachment_set.filter(type=FFD.IMAGE)

    def get_video(self):
        return self.messageattachment_set.filter(type=FFD.VIDEO)

    def get_audio(self):
        return self.messageattachment_set.filter(type=FFD.AUDIO)

    def get_files(self):
        return self.messageattachment_set.filter(type=FFD.FILES)


class MessageAttachment(models.Model):
    parent = models.ForeignKey(Message, on_delete='Cascade')
    type = models.CharField(max_length=2,
                            choices=FFD.FILE_TYPE)
    file = models.FileField(upload_to='chat_data/files/',
                            blank=True)
