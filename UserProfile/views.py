from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, JsonResponse, QueryDict, HttpRequest
from django.template.loader import render_to_string

from UserProfile.forms import *
from UserProfile.models import UserExt, save_attach

from datetime import datetime

from Lib.FileFormats import handle_uploaded_file



# Create your views here.


def home(request, user_id):
    user = get_object_or_404(UserExt, pk=user_id)

    try:
        user_info = UserInfo.objects.get(pk=user.pk)
    except UserInfo.DoesNotExist:
        user_info = None

    status = 'none'
    if user_info:
        status = user.userinfo.STATUS_TYPE[request.user.userinfo.status]

    notes = user.get_new_note_portion()


    data = {
        'user': user,
        'status': status,
        'is_owner': False,
        'notes': notes,
            }

    if user_id == request.user.pk:
        data['is_owner'] = True

    return render(request, "UserProfile/home.html", data)


def load_notes(request, user_id):
    user = get_object_or_404(UserExt, pk=user_id)
    if request.is_ajax():

        since = None
        if 'since' in request.GET:
            since = datetime.strptime(request.GET['since'], '%d-%m-%Y %H:%M')

        notes = user.get_new_note_portion(since)

        data = {
            'notes': notes,
        }
        page = render_to_string('UserProfile/notes_list.html', data)
        response = {'html': page}
        return JsonResponse(response)

    return Http404


@login_required
def note_page(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    is_owner = (request.user == note.user)
    data = {
        'note': note,
        'is_owner': is_owner,
    }
    return render(request, 'UserProfile/note_page.html', data)


@login_required
def note_create_page(request):
    user = UserExt.objects.get(pk=request.user.pk)
    errors_file_type = []


    if request.method == 'POST':
        form_note = NoteForm(request.POST)
        form_attach = AttachmentForm(request.POST, request.FILES)

        if form_note.is_valid():
            errors_file_type = (handle_uploaded_file(request.FILES))
            if not len(form_note.cleaned_data['text']) and not (len(request.FILES)):
                errors_file_type.append('Empty post!')

            if not errors_file_type:
                new_note = form_note.save(commit=False)
                new_note.user = user
                new_note.save()

                save_attach(request.FILES, new_note, Attachment)

                if request.is_ajax():
                    print('ajax')
                    return render(request,
                                  'UserProfile/note_block.html',
                                  {'note': new_note,
                                   'is_creating': True,
                                   })

                return HttpResponseRedirect('/user/%s/' % request.user.pk)

            else:
                return JsonResponse({'errors': errors_file_type})

    else:
        print('nore')
        form_note = NoteForm()
        form_attach = AttachmentForm()

    print('render')
    return render(request,
                  'UserProfile/includes/create_note.html',
                  {'form_note': form_note,
                   'form_attach': form_attach,
                   'is_creating': True,
                   'errors_type': errors_file_type,
                   })


@login_required
def note_edit_page(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.user != note.user:
        return Http404

    if request.method == 'POST':
        form_note = NoteForm(request.POST)
        if form_note.is_valid():
            note.text = form_note.cleaned_data['text']
            note.save()
            if request.is_ajax():
                return JsonResponse({'text': note.text,
                                     'status': 'success'})
            return HttpResponseRedirect('/user/%s/' % request.user.pk)
        else:
            if request.is_ajax():
                return JsonResponse({'text': note.text,
                                     'status': 'fail'})
    else:
        form_note = NoteForm(instance=note)

    data = {'form_note': form_note,
            'note': note,
            }
    if request.is_ajax():
        template = 'UserProfile/create_edit_note_block.html'
    else:
        template = 'UserProfile/edit_note.html'
    return render(request, template, data)


def delete_note(request):
    if request.method == 'POST':
        note = Note.objects.get(pk=int(QueryDict(request.body).get('notepk')))
        if request.user == note.user:
            note.deleted = datetime.now()
            note.save()
            response_data = {}
            response_data['msg'] = 'Post was deleted.'
            return JsonResponse(response_data)

    return JsonResponse({"msg": "this isn't happening"})
