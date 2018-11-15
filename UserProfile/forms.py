from django import forms

from UserProfile.models import *


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['user', 'date_public', 'deleted']

        widgets = {
            'text': forms.Textarea(attrs={'name': 'text',
                                          'id': 'id_text',
                                          'maxlength': 1000,
                                          'class': 'form-control h-100',
                                          'rows': False,
                                          'cols': False,
                                          'style': False,
                                          }),
        }


class AttachmentForm(forms.Form):
    images = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'name': 'photo',
                                      'multiple': True,
                                      'class': 'file invisible position-absolute',
                                      'required': False,
                                      'accept': 'image/*'})
    )

    video = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'name': 'video',
                                      'multiple': False,
                                      'class': 'file invisible position-absolute',
                                      'required': False,
                                      'accept': 'video/*'})
    )

    audio = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'name': 'audio',
                                      'multiple': True,
                                      'class': 'file invisible position-absolute',
                                      'required': False,
                                      'accept': 'audio/*'})
    )

    files = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'name': 'files',
                                      'class': 'file invisible position-absolute',

                                      'required': False,
                                      'multiple': True,
                                      })
    )

