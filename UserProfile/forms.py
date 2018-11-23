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


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['title', 'about', 'date_finish', 'photo']

        widgets = {
            'title': forms.TextInput(attrs=
            {
                'class': 'form-control mb-2',
            }),
            'about': forms.Textarea(attrs=
            {
                'maxlength': 1000,
                'class': 'form-control mb-2',
            }),
            'date_finish': forms.DateInput(attrs=
            {
                'class': 'form-control mb-2',
                'placeholder': 'YYYY-MM-DD',
            }),
            'photo': forms.FileInput(attrs=
            {
                'class': 'invisible position-absolute',
                'required': False,
                'accept': 'image/*'
            }),
        }

    def save(self, user, *args, **kwargs):
        diary = super(DiaryForm, self).save(commit=False)
        diary.user = user
        diary.save()
        return diary


class MarkerForm(forms.ModelForm):
    class Meta:
        model = Marker
        fields = ['lat', 'lng']

        # initial = {
        #   'lat' : 52.357971,
        #   'lng' : -6.51675
        # }

        widgets = {
            'lat': forms.TextInput(attrs={
                'class': 'form-control mb-1',
            }),
            'lng': forms.TextInput(attrs={
                'class': 'form-control mb-1',
            })
        }