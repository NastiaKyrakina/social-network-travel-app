from django import forms
from .models import Message, Chat

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']

    def save(self, user, chat, *args, **kwargs):
        message = super(MessageForm, self).save(commit=False)
        message.user = user
        message.chat = chat
        message.save()
        return message


class ChatForm(forms.Form):
    name = forms.CharField()
    chat_type = forms.ChoiceField(choices=Chat.TYPE_CHATS,
                                  widget=forms.RadioSelect)


class ChatMember(forms.Form):
    members = forms.CharField(widget=forms.TextInput(attrs={
        'hide': True,
        'list': 'members_list',
    }))
