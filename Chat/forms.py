from django import forms
from .models import Message, Chat, User

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
    chat_type = forms.ChoiceField(choices=Chat.TYPE_CHATS[1:],
                                  widget=forms.RadioSelect)
    image = forms.FileField()

    def save(self, exs_chat=None):
        chat_name = self.cleaned_data['name']
        chat_type = self.cleaned_data['chat_type']
        image = self.cleaned_data['image']
        if exs_chat:
            exs_chat.name = chat_name
            exs_chat.chat_type = chat_type
            chat = exs_chat
        else:
            chat = Chat(name=chat_name, chat_type=chat_type, image=image)
        chat.save()
        return chat


class ChatMember(forms.Form):
    members = forms.CharField(widget=forms.TextInput(attrs={
        'list': 'members_list',
    }))

    def members_list(self):
        members = self.cleaned_data['members']
        member_list = []
        if members:
            print(type(members))
            members_set = members.split(',')
            for member in members_set:
                try:
                    opponent = User.objects.get(username=member)
                    member_list.append(opponent)

                except User.DoesNotExist:
                    return forms.ValidationError('User %s does not exist' % member,
                                                 code='13')

        return member_list

    def clean_members(self):
        return self.members_list()
