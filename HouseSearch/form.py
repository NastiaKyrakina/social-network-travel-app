from django import forms
from django.db.models import Max
from UserProfile.models import Country
from HouseSearch.models import House, HousePhoto, Rate, \
    MAX_PRICE, MAX_ROOMS, MAX_SLEEPER




class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['title', 'country', 'city', 'address', 'type',
                  'rooms', 'sleeper', 'price', 'activity', 'about']


        widgets = {
            'title': forms.TextInput(attrs={

                'required': True,
                'class': 'form-control mb-2',
                'placeholder': 'Title',
                'title': 'Enter title of advertisement',
                'maxlength': 100,

            }),

            # pattern = "[\+]\d{1}\s[\(]\d{3}[\)]\s\d{3}[\-]\d{2}[\-]\d{2}"
            'city': forms.TextInput(attrs={
                'name': 'city',
                'class': 'form-control mb-2',
                'placeholder': 'City',
                'title': 'Enter city: only alphabet character valid',
                'maxlength': 40,
                'pattern': '[A-Za-zА-ЯЙйЁёЫыъьІіЄєЇї]*[ -`][A-Za-zА-ЯЙйЁёЫыъьІіЄєЇї]*',

            }),
            'address': forms.TextInput(attrs={
                'name': 'Address',
                'class': 'form-control mb-2',
                'placeholder': 'Street, 1, 1',
                'title': 'Enter address: Street Name, House Number, Apartment Number',
                'maxlength': 100,
                'pattern': '[A-Za-zА-ЯЙйЁёЫыъьІіЄєЇї][A-Za-zА-ЯЙйЁёЫыъьІіЄєЇї`- ],'
            }),
            'type': forms.Select(choices=House.HOUSE_TYPE,
                                 attrs={
                                     'class': 'form-control mb-2',
                                     'name': 'type',
                                     'title': 'Select house-type',
                                 }),
            'rooms': forms.NumberInput(attrs={
                'name': 'rooms',
                'class': 'form-control mb-2',
                'title': 'Enter rooms count',
                'min': 1,
                'max': MAX_ROOMS,
            }),

            'price': forms.NumberInput(attrs={
                'name': 'price',
                'class': 'form-control',
                'title': 'Enter maximum price',
                'value': 100,
                'min': 1,
                'max': MAX_PRICE,
            }),
            'sleeper': forms.NumberInput(attrs={
                'name': 'sleeper',
                'class': 'form-control mb-2',
                'required': False,
                'title': 'Enter sleeper count',
                'min': 1,

            }),

            'about': forms.Textarea(attrs={
                'name': 'about',
                'class': 'form-control mb-2',
                'title': 'Tell about house',
                'placeholder': 'Tell about house...',
            }),

            'activity': forms.CheckboxInput(attrs={
                'class': 'custom-control-input',
            }),
        }


    def save(self, user):
        house = super(HouseForm, self).save(commit=False)
        house.owner = user
        house.save()
        return house


class PhotoForm(forms.ModelForm):
    class Meta:
        model = HousePhoto
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs=
                                     {'name': 'photo',
                                      'class': 'house-edit-images invisible position-absolute',
                                      'multiple': True,
                                      'required': False,
                                      'accept': 'image/*'})
        }



class SearchHousesForm(forms.Form):
    country = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'name': 'country',
            'required': False,
            'placeholder': 'Country',
            'title': 'Choice country for search',
            'maxlength': 30,
            'list': 'countries'
        })
    )

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'name': 'city',
            'required': False,
            'placeholder': 'City',
            'title': 'Enter city name for search',
            'maxlength': 40,
        })
    )

    type = forms.MultipleChoiceField(
        required=False,
        choices=House.HOUSE_TYPE,
        widget=forms.CheckboxSelectMultiple(attrs={
            'name': 'type',
            'required': False,
            'checked': True,
            'title': 'Choice house-types for search',
        })
    )
    min_price = forms.DecimalField(
        label='From',
        required=False,
        initial=0.00,
        widget=forms.NumberInput(attrs={
            'name': 'min_price',
            'required': False,
            'title': 'Enter minimum price',
            'min': 0,
            'max': MAX_PRICE,
        })
    )
    max_price = forms.DecimalField(
        label='To',
        required=False,
        initial=MAX_PRICE,
        widget=forms.NumberInput(attrs={
            'name': 'max_price',
            'required': False,
            'title': 'Enter maximum price',
            'min': 0,
            'max': House.objects.aggregate(Max('price'))['price__max'],
        })
    )
    rooms = forms.IntegerField(
        required=False,
        initial=1,
        widget=forms.NumberInput(attrs={
            'name': 'rooms',
            'required': False,
            'title': 'Enter rooms count',
            'min': 1,
            'max': House.objects.aggregate(Max('rooms'))['rooms__max'],
        })
    )

    sleeper = forms.IntegerField(
        required=False,
        initial=1,
        widget=forms.NumberInput(attrs={
            'name': 'sleeper',
            'required': False,
            'title': 'Enter sleeper count',
            'min': 1,
            'max': House.objects.aggregate(Max('sleeper'))['sleeper__max'],
        })

    )
    active = forms.BooleanField(
        label='Only active',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'name': 'active',
            'required': False,
            'title': 'Search only acrive advertisement',
        })
    )
    public = forms.DateField(
        required=False,
        widget=forms.SelectDateWidget(attrs={
            'name': 'public',
            'required': False,
            'title': 'Search advertisement',
        })

    )

    text = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'name': 'text',
            'required': False,
            'id': 'hide-text',
        })

    )

    def get_only_full(self):
        """Очистка списка значений полей от пустых полей"""
        dict = self.cleaned_data.copy()

        for key in self.cleaned_data:
            if not (dict[key]) and key != 'type':
                del dict[key]
        return dict


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = ['comment', 'value']

    def save(self, user, house):
        new_rate = super(RateForm, self).save(commit=False)
        new_rate.user = user
        new_rate.house = house
        print(new_rate)
        new_rate.save()
        return new_rate
