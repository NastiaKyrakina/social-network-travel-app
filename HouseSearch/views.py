from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse, QueryDict, HttpRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from UserProfile.models import UserExt, Country
from .models import House, HousePhoto, MAX_USER_HOUSES
from .form import HouseForm, PhotoForm, SearchHousesForm, RateForm
from datetime import datetime
from Lib import FileFormats, page_revisor

from django.db.models import Avg


def rate_create(request, house_id):
    house = get_object_or_404(House, id=house_id)
    user = UserExt.objects.get(pk=request.user.pk)

    if request.method == 'POST':
        form_rate = RateForm(request.POST)
        if form_rate.is_valid():
            rate = form_rate.save(user, house)
            print(rate)
            if request.is_ajax():
                return render(request,
                              'HouseSerch/includes/rate-block.html',
                              {'rate': rate,
                               }
                              )
            return HttpResponseRedirect('house/%s/' % house.pk)
    else:
        form_rate = RateForm()

    return render(request, 'HouseSerch/includes/form_rate_block.html', {
        'form_rate': form_rate,
    })


def main_search(request):
    if 'text' in request.GET:
        print(request.GET['text'])

    return HttpResponseRedirect('/house/')


def user_houses(request):
    if 'user' in request.GET:
        user = get_object_or_404(UserExt, id=request.GET['user'])
        houses = House.objects.filter(owner=user)


def house_search_page(request):
    if 'reset' in request.GET:
        return HttpResponseRedirect(request.path)

    request.META['QUERY_STRING'] = \
        page_revisor.remove_page(request.META['QUERY_STRING'])

    houses = House.objects.all()
    form_search = SearchHousesForm()

    if 'text' in request.GET and request.GET['text']:
        houses = House.objects.ft_search(request.GET.dict()['text'])

    if 'country' in request.GET:
        form_search = SearchHousesForm(request.GET)

        if form_search.is_valid():
            print(form_search.cleaned_data)
            dict = form_search.get_only_full()

            if len(dict):
                houses = House.objects.multi_search(houses, dict)

    context = {
        'form_search': form_search,
    }

    if houses:
        print('Has result')
        message = "Result: " + str(houses.count())

        paginator = Paginator(houses, 2)
        page = request.GET.get('page')

        try:
            houses_page = paginator.page(page)
        except PageNotAnInteger:
            houses_page = paginator.page(1)
        except EmptyPage:
            houses_page = paginator.page(paginator.num_pages)

        context['houses'] = houses_page

    else:
        message = "No result :("

    context['message'] = message

    return render(request, 'HouseSerch/house_search.html', context)


def house_page(request, house_id):
    house = get_object_or_404(House, id=house_id)
    is_owner = (request.user == house.owner)
    type = house.HOUSE_TYPE[house.type]
    raiting = house.rate_set.aggregate(Avg('value'))
    data = {
        'type': type,
        'house': house,
        'is_owner': is_owner,
        'raiting': raiting['value__avg']

    }
    return render(request, 'HouseSerch/house_page.html', data)


def house_add_page(request):
    user = UserExt.objects.get(pk=request.user.pk)

    if user.house_set.count() == MAX_USER_HOUSES:
        return render(request, 'HouseSerch/limit_house.html', {user: user})

    errors_file_type = []

    if request.method == 'POST':
        form_house = HouseForm(request.POST)
        form_photo = PhotoForm(request.POST, request.FILES)
        if form_house.is_valid() and form_photo.is_valid():
            errors_file_type = FileFormats.handle_uploaded_file(request.FILES)
            if not errors_file_type:
                new_house = _home_save(request, form_house, user)
                return HttpResponseRedirect('/house/%s/' % new_house.id)
        else:
            print(form_house.errors)
    else:
        form_house = HouseForm()
        form_photo = PhotoForm()

    return render(request,
                  'HouseSerch/add_house.html',
                  {'form_house': form_house,
                   'form_photo': form_photo,
                   'is_creating': True,
                   'errors_type': errors_file_type,
                   })


def _home_save(request, form_house, user):
    new_house = form_house.save(user)
    files = request.FILES.getlist('image', None)
    for file in files:
        new_house_photo = HousePhoto(house=new_house, image=file)
        new_house_photo.save()
    return new_house


def house_edit_page(request, house_id):
    house = get_object_or_404(House, id=house_id)
    user = UserExt.objects.get(pk=request.user.pk)

    if user != house.owner:
        return Http404

    errors_file_type = []
    if request.method == 'POST':
        form_house = HouseForm(request.POST, instance=house)
        form_photo = PhotoForm(request.POST, request.FILES)
        if form_house.is_valid() and form_photo.is_valid():
            errors_file_type = FileFormats.handle_uploaded_file(request.FILES)
            if not errors_file_type:
                new_house = _home_save(request, form_house, user)
                return HttpResponseRedirect('/house/%s/' % new_house.id)
    else:
        form_house = HouseForm(instance=house)
        form_photo = PhotoForm()

    return render(request,
                  'HouseSerch/add_house.html',
                  {'form_house': form_house,
                   'form_photo': form_photo,
                   'house': house,
                   'errors_type': errors_file_type,
                   })


def house_delete(request):
    if request.method == 'POST':
        house = House.objects.get(pk=int(QueryDict(request.body).get('housepk')))
        if request.user == house.owner:
            house.deleted = datetime.now()
            house.save()
            response_data = {}
            response_data['msg'] = 'Post was deleted.'
            return JsonResponse(response_data)

    return JsonResponse({"msg": "this isn't happening"})
