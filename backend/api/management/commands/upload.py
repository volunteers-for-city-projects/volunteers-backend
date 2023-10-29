import csv
import os

from django.core.management.base import BaseCommand

from content.models import City, Skills, Valuation  # , News

# from projects.models import Category


def load_cities():
    print('loading cities...')
    cities = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/cities.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), 'data', 'cities.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            city = City(
                name=row[1],
            )
            cities.append(city)
        City.objects.bulk_create(cities)
    print('cities loaded!')


def load_skills():
    print('loading skills...')
    skills = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/skills.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), 'data', 'skills.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            skill = Skills(
                name=row[1],
            )
            skills.append(skill)
        Skills.objects.bulk_create(skills)
    print('skills loaded!')

# def load_categories():
#    print('loading categories...')
#    categories = []
#    #  путь для заливки на сервер не проверен
#    # file_path = "/app/data/categories.csv"   путь для заливки на сервер
#    file_path = os.path.join(os.getcwd(), '..', 'data', 'categories.csv')
#    with open(file_path, encoding="utf-8-sig") as file:
#        reader = csv.reader(file)
#        for row in reader:
#            category = Category(
#                name=row[1],
#                slug=row[2],
#                description=row[3],
#            )
#            categories.append(category)
#        Category.objects.bulk_create(categories)
#    print('categories loaded!')

# def load_news():
#    print('loading news...')
#    news = []
#    #  путь для заливки на сервер не проверен
#    # file_path = "/app/data/news.csv"   путь для заливки на сервер
#    file_path = os.path.join(os.getcwd(), '..', 'data', 'news.csv')
#    with open(file_path, encoding="utf-8-sig") as file:
#        reader = csv.reader(file)
#        for row in reader:
#            new = News(
#                title=row[1],
#                text=row[2],
#            )
#            news.append(new)
#        News.objects.bulk_create(news)
#    print('news loaded!')


def load_valuations():
    print('loading valuations...')
    valuations = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), 'data', 'valuations.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            valuation = Valuation(
                title=row[1],
                description=row[2],
            )
            valuations.append(valuation)
        Valuation.objects.bulk_create(valuations)
    print('valuations loaded!')


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            load_cities()
            load_skills()
#            load_categories()
#            load_news()
            load_valuations()
        except Exception as error:
            print(error)
