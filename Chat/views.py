from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, QueryDict, HttpRequest
from django.contrib.auth.decorators import login_required
from UserProfile.models import UserExt, save_attach
from .models import Chat, Message, Member, MessageAttachment
from UserProfile.forms import AttachmentForm
from .forms import MessageForm
from django.utils.safestring import mark_safe
import json
from datetime import datetime

from Lib.FileFormats import handle_uploaded_file


def chat_list(request):
    user = UserExt.objects.get(id=request.user.id)
    chats = Chat.chat_objects.users_chats(user.id)
    context = {
        'chats': chats,
    }
    return render(request, 'Chat/chats_page.html', context)


def chat_block(request, chat_slug):
    user = UserExt.objects.get(id=request.user.id)
    chat = get_object_or_404(Chat, slug=chat_slug)
    try:
        chat.members.get(id=user.id)
    except Chat.DoesNotExist:
        return None

    if 'since' in request.GET:
        date_since = datetime.strptime(request.GET['since'], '%d-%m-%Y %H:%M')
        messages = Message.message_object.last_10_messages(chat, date_since)
        print(messages)
        return render(request, 'Chat/messages_list.html', {'messages': messages})

    messages = Message.objects.filter(chat=chat).order_by('-date')[0:10]

    context = {
        'chat': chat,
        'messages': messages
    }
    return render(request, 'Chat/chat_block.html', context)


def create_message(request):

    user = UserExt.objects.get(id=request.user.id)

    print(request.POST)
    print(request.FILES)
    errors_file_type = []

    if request.method == 'POST':

        chat = get_object_or_404(Chat, slug=request.POST['chat_slug'])

        form_message = MessageForm(request.POST)
        form_attach = AttachmentForm(request.FILES)

        if form_message.is_valid():
            errors_file_type = (handle_uploaded_file(request.FILES))
            if not len(form_message.cleaned_data['text']) and not (len(request.FILES)):
                errors_file_type.append('empty')
            else:
                message = form_message.save(user, chat)
                save_attach(request.FILES, message, MessageAttachment)

                return JsonResponse({'message': message.id})
    else:
        form_message = MessageForm()
        form_attach = AttachmentForm()

    return render(request, 'Chat/form_message_block.html', {
        'form_message': form_message,
        'form_attach': form_attach,
        'errors_file_type': errors_file_type
    })
