from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, QueryDict, HttpRequest

from UserProfile.models import UserExt
from .models import Chat, Message, Member
from .forms import MessageForm
from django.utils.safestring import mark_safe
import json

def chat_list_page(request):
    """"Чат поиск"""
    return render(request, 'Chat/chat_select')

def chat_page(request, room_name):
    """"Чат"""
    return render(request, 'Chat/chat_room.html',
                  {
                      'room_name_json': mark_safe(json.dumps(room_name))
                  }
                  )


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
    messages = Message.objects.filter(chat=chat)
    context = {
        'chat': chat,
        'messages': messages
    }
    return render(request, 'Chat/chat_block.html', context)


def create_message(request, chat_slug):
    user = UserExt.objects.get(id=request.user.id)
    chat = get_object_or_404(Chat, slug=chat_slug)

    if request.method == 'POST':
        form_message = MessageForm(request.POST)
        if form_message.is_valid():
            message = form_message.save(user, chat)
            print(message)
            return render(request,
                          'Chat/message_block.html',
                          {
                              'message': message,
                          }
                          )

    else:
        form_message = MessageForm()

    return render(request, 'Chat/form_message_block.html', {
        'form_message': form_message,
    })
