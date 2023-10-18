import os
import csv

from django.core.management.base import BaseCommand

from content.models import City, Skills
from projects.models import Category

# import os # путь локально расскоментировать




def load_cities():
    print('loading cities...')
    cities = []
    file_path = os.path.join(os.getcwd(), '..', 'data', 'cities.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            city = City(
                name=row['name'],
            )
            cities.append(city)
        City.objects.bulk_create(cities)
    print('cities loaded!')


def load_skills():
    print('loading skills...')
    skills = []
    file_path = os.path.join(os.getcwd(), '..', 'data', 'skills.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            skill = Skills(
                name=row['name'],
            )
            skills.append(skill)
        City.objects.bulk_create(skills)
    print('skills loaded!')


def load_categories():
    print('loading categories...')
    categories = []
    file_path = os.path.join(os.getcwd(), '..', 'data', 'categories.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            category = Category(
                name=row['name'],
                description=row['description'],
            )
            categories.append(category)
        City.objects.bulk_create(categories)
    print('categories loaded!')

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            load_cities()
            load_skills()
            load_categories()
        except Exception as error:
            print(error)
