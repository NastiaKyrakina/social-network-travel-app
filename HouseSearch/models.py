from django.db import models
from django.contrib.auth.models import User
from model_utils import Choices
from UserProfile.models import Country

from django.urls import reverse
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

def get_sentinel_country():
    return Country.objects.get_or_create(name='deleted')[0]


class HouseManager(models.Manager):

    def get_queryset(self):
        return super(HouseManager, self).get_queryset().filter(deleted__isnull=True)

    def ft_search(self, text):
        query_world = [world for world in text.split(' ') if world]

        if not query_world:
            return None

        s_title = SearchVector('title')
        s_country = SearchVector('country__name')
        s_city = SearchVector('city')
        s_about = SearchVector('about')

        qfilter = SearchQuery(query_world[0])

        if len(query_world) > 1:
            for q in query_world:
                qfilter |= SearchQuery(q)

        houses = House.objects. \
            annotate(search=s_title + s_country + s_city + s_about). \
            filter(search=qfilter).order_by('-date_public')

        print(houses)
        return houses

    def multi_search(self, houses, kwargs):
        print(houses)
        print(kwargs)
        if 'min_price' in kwargs:
            houses = houses.filter(price__gt=kwargs['min_price'])
        if 'max_price' in kwargs:
            houses = houses.filter(price__lt=kwargs['max_price'])
        if 'country' in kwargs:
            houses = houses.filter(country__name=kwargs['country'])
        if 'type' in kwargs:
            print(kwargs['type'])
            for type in House.HOUSE_TYPE:
                if not (type[0] in kwargs['type']):
                    houses = houses.exclude(type=type[0])

        if 'city' in kwargs:
            houses = houses.filter(city=kwargs['city'])
        if 'rooms' in kwargs:
            houses = houses.filter(rooms=kwargs['rooms'])
        if 'sleeper' in kwargs:
            houses = houses.filter(sleeper=kwargs['sleeper'])
        if 'public' in kwargs:
            houses = houses.filter(date_public__gt=kwargs['public'])
        if 'active' in kwargs:
            if kwargs['active']:
                houses = houses.filter(activity=True)

        return houses


class HouseDeleteManager(models.Manager):

    def get_queryset(self):
        return super(HouseDeleteManager, self).get_queryset().filter(deleted__isnull=False).order_by('-deleted')


MAX_USER_HOUSES = 20
MAX_PRICE = 999.99
MAX_ROOMS = 50
MAX_SLEEPER = 100

class House(models.Model):

    PRIVATE_HOUSE = 'PH'
    APARTMENT = 'AP'
    VILLA = 'VL'

    HOUSE_TYPE = Choices(
        (PRIVATE_HOUSE, 'Private house'),
        (APARTMENT, 'Apartment'),
        (VILLA, 'Villa'),
    )
    """Owner user"""
    owner = models.ForeignKey(User, on_delete='Cascade')

    title = models.CharField(max_length=100, blank=True)

    """Piece of address"""
    country = models.ForeignKey(Country, on_delete=models.SET(get_sentinel_country))
    city = models.CharField(max_length=40)
    address = models.CharField(max_length=100)

    """Describe house"""
    type = models.CharField(max_length=2, choices=HOUSE_TYPE, default=PRIVATE_HOUSE)
    rooms = models.SmallIntegerField(default=1)
    sleeper = models.SmallIntegerField(default=1)
    about = models.TextField(max_length=500)

    price = models.DecimalField(decimal_places=2, max_digits=10)

    activity = models.BooleanField(default=True)
    date_public = models.DateField(auto_now_add=True)
    deleted = models.DateField(null=True, blank=True, db_index=True)

    objects = HouseManager()
    house_delete_objects = HouseDeleteManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('house', args=[str(self.id)])

    def get_images(self):
        return self.housephoto_set.all()

    def main_image(self):
        main_image = self.housephoto_set.first()
        if main_image:
            return main_image.image.url
        return None


class HousePhoto(models.Model):
    house = models.ForeignKey(House, on_delete='Cascade')
    image = models.ImageField(upload_to='house_data/photo/', blank=True)

    def __str__(self):
        return self.image.path


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete='Cascade')
    house = models.ForeignKey(House, on_delete='Cascade')
    value = models.DecimalField(decimal_places=1, max_digits=2)
    comment = models.TextField(max_length=1000)
    date_public = models.DateField(auto_now=True)
    correct = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.user.username + ' | ' + self.house.title
