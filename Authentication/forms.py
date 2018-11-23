from django import forms
import re
from UserProfile.models import User, UserInfo, UserExt


class AuthorizationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    password = forms.CharField(
        label='Passport',
        widget=forms.PasswordInput()
    )


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='Last name', max_length=30)
    last_name = forms.CharField(label='First name', max_length=30)
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

        new_user = UserExt.objects.create_user(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
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
            'gender': forms.RadioSelect(choices=GENDER_SELECT, attrs={
                'class': 'custom-control-input',
            }),
            'birthday': forms.DateInput(attrs={
                'class': 'form-control mb-2'
            }),
            'status': forms.Select(choices=UserInfo.STATUS_TYPE, attrs={
                'class': 'custom-select',
            }),
            'phone_num': forms.TextInput(attrs={
                'class': 'form-control mb-2'
            }),
            'country': forms.TextInput(attrs={
                'name': 'country',
                'required': True,
                'class': 'form-control mb-2',
                'placeholder': 'Country',
                'title': 'Enter country for search',
                'maxlength': 30,
                'list': 'countries'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control mb-2',
            }),
            'info': forms.Textarea(attrs=
            {
                'maxlength': 1000,
                'class': 'form-control mb-2',
                'rows': '4',
            }),
            'big_photo': forms.FileInput(attrs=
            {
                'class': 'invisible position-absolute',
                'required': False,
                'accept': 'image/*'
            }),
       }

    def save(self, user):
        user_info = super(InformationForm, self).save(commit=False)
        user_info.user = user
        return user_info.save()