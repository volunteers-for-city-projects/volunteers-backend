import csv

from django.core.management.base import BaseCommand

from content.models import City

# import os # путь локально расскоментировать




def load_cities():
    print('loading cities...')
    cities = []
    #  путь для заливки на сервер не проверен
    file_path = "/app/data/cities.csv"  # путь для заливки на сервер
    # file_path = os.path.join(os.getcwd(), '..', 'data', 'cities.csv')  # путь локально расскомментировать
    with open(file_path, encoding="utf-8-sig") as file:
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
