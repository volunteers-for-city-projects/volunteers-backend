import csv

from django.core.management.base import BaseCommand

from content.models import City


def load_cities():
    print('loading cities...')
    cities = []
    with open("/app/data/cities.csv", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            city = City(
                name=row[0],
            )
            cities.append(city)
        City.objects.bulk_create(cities)
    print('cities loaded!')


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            load_cities()
        except Exception as error:
            print(error)
