from django import forms
import re
from UserProfile.models import User, UserInfo


class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(
        label='Passport',
        widget=forms.PasswordInput()
    )


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        label='Passport',
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='Passport (again)',
        widget=forms.PasswordInput()
    )

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        return forms.ValidationError('Passwords do not match')

    def clear_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        return forms.ValidationError('Username is already taken.')

    def save(self):

        new_user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )

        return new_user


class InformationForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        exclude = ['user', 'registration', 'last_visit']

        GENDER_SELECT = (
            (0, 'male'),
            (1, 'female')
        )

        widgets = {
            'gender': forms.RadioSelect(choices=GENDER_SELECT),
            'birthday': forms.DateInput,
            'status': forms.Select(choices=UserInfo.STATUS_TYPE),
            'phone_num': forms.TextInput,
            'country': forms.TextInput(attrs={
                'name': 'country',
                'required': True,
                'class': '',
                'placeholder': 'Country',
                'title': 'Enter country for search',
                'maxlength': 30,
                'list': 'countries'
            }),
            'city': forms.TextInput,
            'info': forms.Textarea,
            'big_photo': forms.FileInput(),
       }

    def save(self, user):
        user_info = super(InformationForm, self).save(commit=False)
        user_info.user = user
        return user_info.save()
