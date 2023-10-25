import csv
import os

from django.core.management.base import BaseCommand

from content.models import City, Skills, News, Valuation
from projects.models import Category, Organization, Volunteer, VolunteerSkills
from users.models import User

# import os # путь на сервер расскоментировать

def load_cities():
    print('loading cities...')
    cities = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/cities.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), '..', 'data', 'cities.csv')
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
    file_path = os.path.join(os.getcwd(), '..', 'data', 'skills.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            skill = Skills(
                name=row[1],
            )
            skills.append(skill)
        Skills.objects.bulk_create(skills)
    print('skills loaded!')

def load_categories():
    print('loading categories...')
    categories = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/categories.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), '..', 'data', 'categories.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            category = Category(
                name=row[1],
                slug=row[2],
                description=row[3],
            )
            categories.append(category)
            Category.objects.bulk_create(categories)
    print('categories loaded!')

def load_news():
    print('loading news...')
    news = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/news.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), '..', 'data', 'news.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            new = News(
                title=row[1],
                text=row[2],
                created_at=row[3],
                tags=row[4],
                author_id=row[5],
            )
            news.append(new)
        News.objects.bulk_create(news)
    print('news loaded!')

def load_valuations():
    print('loading valuations...')
    valuations = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), '..', 'data', 'valuations.csv')
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

def load_users():
    print('loading users...')
    users = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), '..', 'data', 'users.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            user = User(
                first_name=row[1],
                last_name=row[2],
                second_name=row[3],
                email=row[4],
                role=row[5],
            )
            users.append(user)
        User.objects.bulk_create(users)
    print('users loaded!')

def load_organizations():
    print('loading organizations...')
    organizations = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), '..', 'data', 'organizations.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            organization = Organization(
                title=row[1],
                ogrn=row[2],
                phone=row[3],
                about=row[4],
                city_id=row[5],
                contact_person_id=row[6]
            )
            organizations.append(organization)
        Organization.objects.bulk_create(organizations)
    print('organizations loaded!')

def load_volunteers():
    print('loading volunteers...')
    volunteers = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), '..', 'data', 'volunteers.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            volunteer = Volunteer(
                telegram=row[1],
                data_of_birth=row[3],
                phone=row[4],
                city_id=row[5],
                user_id=row[6],
            )
            volunteers.append(volunteer)
        Volunteer.objects.bulk_create(volunteers)
    print('volunteers loaded!')

def load_volunteerskills():
    print('loading volunteerskills...')
    volunteerskills = []
    #  путь для заливки на сервер не проверен
    # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
    file_path = os.path.join(os.getcwd(), '..', 'data', 'volunteerskills.csv')
    with open(file_path, encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for row in reader:
            volunteerskill = VolunteerSkills(
                volunteer_id=row[1],
                skills_id=row[2],
            )
            volunteerskills.append(volunteerskill)
        VolunteerSkills.objects.bulk_create(volunteerskills)
    print('volunteerskills loaded!')

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            load_cities()
            load_skills()
            load_categories()
            load_news()
            load_valuations()
            load_users()
            load_organizations()
            load_volunteers()
            load_volunteerskills()
        except Exception as error:
            print(error)
