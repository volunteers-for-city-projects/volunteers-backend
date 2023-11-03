import os
from csv import DictReader

from django.core.management.base import BaseCommand

from content.models import City, News, Skills, Valuation
from projects.models import (
    Category,
    Organization,
    Project,
    ProjectCategories,
    ProjectParticipants,
    ProjectSkills,
    Volunteer,
    VolunteerSkills,
)
from users.models import User

TABLES_DICT = {
    City: 'cities.csv',
    Skills: 'skills.csv',
    Category: 'categories.csv',
    Valuation: 'valuations.csv',
    User: 'users.csv',
    News: 'news.csv',
    Organization: 'organizations.csv',
    Volunteer: 'volunteers.csv',
    VolunteerSkills: 'volunteerskills.csv',
    Project: 'projects.csv',
    ProjectCategories: 'projectcategories.csv',
    ProjectSkills: 'projectskills.csv',
    ProjectParticipants: 'projectparticipants.csv'
}


class Command(BaseCommand):
    help = 'Load data from csv files'

    def handle(self, *args, **kwargs):
        for model, base in TABLES_DICT.items():
            try:
                file_path = os.path.join(os.getcwd(), 'data', f'{base}')
                with open(file_path, encoding="utf-8-sig") as csv_file:
                    reader = DictReader(csv_file)
                    model.objects.bulk_create(model(**data) for data in reader)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully load table'
                            f'of model {model.__name__}'
                        )
                    )
            except Exception as error:
                self.stdout.write(
                    self.style.ERROR(f'{error} for model {model.__name__}')
                )
        self.stdout.write(self.style.SUCCESS('Finish load data'))

# def load_cities():
#     print('loading cities...')
#     cities = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/cities.csv"   путь для заливки на сервер
#     file_path = os.path.join(os.getcwd(), 'data', 'cities.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             city = City(
#                 id=row['id'],
#                 name=row['name'],
#             )
#             cities.append(city)
#         City.objects.bulk_create(cities)
#     print('cities loaded!')


# def load_skills():
#     print('loading skills...')
#     skills = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/skills.csv"   путь для заливки на сервер
#     file_path = os.path.join(os.getcwd(), 'data', 'skills.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             skill = Skills(
#                 id=row['id'],
#                 name=row['name'],
#             )
#             skills.append(skill)
#         Skills.objects.bulk_create(skills)
#     print('skills loaded!')


# def load_categories():
#     print('loading categories...')
#     categories = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/categories.csv"   путь для заливки на сервер
#     file_path = os.path.join(os.getcwd(), 'data', 'categories.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             category = Category(
#                 id=row['id'],
#                 name=row['name'],
#                 slug=row['slug'],
#                 description=row['description'],
#             )
#             categories.append(category)
#             Category.objects.bulk_create(categories)
#     print('categories loaded!')


# def load_news():
#     print('loading news...')
#     news = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/news.csv"   путь для заливки на сервер
#     file_path = os.path.join(os.getcwd(), 'data', 'news.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             new = News(
#                 id=row['id'],
#                 title=row['title'],
#                 text=row['text'],
#                 created_at=row['created_at'],
#                 tags=row['tags'],
#                 author_id=row['author_id'],
#             )
#             news.append(new)
#         News.objects.bulk_create(news)
#     print('news loaded!')


# def load_valuations():
#     print('loading valuations...')
#     valuations = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
#     file_path = os.path.join(os.getcwd(), 'data', 'valuations.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             valuation = Valuation(
#                 id=row['id'],
#                 title=row['title'],
#                 description=row['description'],
#             )
#             valuations.append(valuation)
#         Valuation.objects.bulk_create(valuations)
#     print('valuations loaded!')


# def load_users():
#     print('loading users...')
#     users = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
#     file_path = os.path.join(os.getcwd(), 'data', 'users.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             user = User(
#                 id=row['id'],
#                 first_name=row['first_name'],
#                 last_name=row['last_name'],
#                 second_name=row['second_name'],
#                 email=row['email'],
#                 role=row['role'],
#             )
#             users.append(user)
#         User.objects.bulk_create(users)
#     print('users loaded!')


# def load_organizations():
#     print('loading organizations...')
#     organizations = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
#     file_path = os.path.join(os.getcwd(), 'data', 'organizations.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             organization = Organization(
#                 id=row['id'],
#                 title=row['title'],
#                 ogrn=row['ogrn'],
#                 phone=row['phone'],
#                 about=row['about'],
#                 city_id=row['city_id'],
#                 contact_person_id=row['contact_person_id'],
#             )
#             organizations.append(organization)
#         Organization.objects.bulk_create(organizations)
#     print('organizations loaded!')


# def load_volunteers():
#     print('loading volunteers...')
#     volunteers = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
#     file_path = os.path.join(os.getcwd(), 'data', 'volunteers.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             volunteer = Volunteer(
#                 id=row['id'],
#                 telegram=row['telegram'],
#                 date_of_birth=row['date_of_birth'],
#                 phone=row['phone'],
#                 city_id=row['city_id'],
#                 user_id=row['user_id'],
#             )
#             volunteers.append(volunteer)
#         Volunteer.objects.bulk_create(volunteers)
#     print('volunteers loaded!')


# def load_volunteerskills():
#     print('loading volunteerskills...')
#     volunteerskills = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/valuations.csv"   путь для заливки на сервер
#     file_path = os.path.join(os.getcwd(), 'data', 'volunteerskills.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             volunteerskill = VolunteerSkills(
#                 id=row['id'],
#                 volunteer_id=row['volunteer_id'],
#                 skill_id=row['skills_id'],
#             )
#             volunteerskills.append(volunteerskill)
#         VolunteerSkills.objects.bulk_create(volunteerskills)
#     print('volunteerskills loaded!')


# def load_projects():
#     print('loading projects...')
#     projects = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/projects.csv"   путь для заливки на сервер
#     file_path = os.path.join(os.getcwd(), 'data', 'projects.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             project = Project(
#                 id=row['id'],
#                 name=row['name'],
#                 description=row['description'],
#                 start_datatime=row['start_datatime'],
#                 end_datatime=row['end_datatime'],
#                 application_date=row['application_date'],
#                 event_purpose=row['event_purpose'],
#                 organization_id=row['organization_id'],
#                 city_id=row['city_id'],
#                 category_id=row['category_id'],
#                 status_project=row['status_project'],
#                 # participants=row['participants'],
#                 status_approve=row['status_approve'],
#             )
#             projects.append(project)
#         Project.objects.bulk_create(projects)
#     print('projects loaded!')


# def load_projectparticipants():
#     print('loading projectparticipants...')
#     projectparticipants = []
#     #  путь для заливки на сервер не проверен
#     # file_path = "/app/data/projectparticipants.csv"   путь для заливки на
#     file_path = os.path.join(os.getcwd(), 'data', 'projectparticipants.csv')
#     with open(file_path, encoding="utf-8-sig") as file:
#         reader = DictReader(file)
#         for row in reader:
#             projectparticipant = ProjectParticipants(
#                 id=row['id'],
#                 project_id=row['project_id'],
#                 volunteer_id=row['volunteer_id'],
#             )
#             projectparticipants.append(projectparticipant)
#         ProjectParticipants.objects.bulk_create(projectparticipants)
#     print('projectparticipants loaded!')


# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         try:
#             load_cities()
#             load_skills()
#             load_categories()
#             load_users()
#             load_news()
#             load_valuations()
#             load_organizations()
#             load_volunteers()
#             load_volunteerskills()
#             load_projects()
#             load_projectparticipants()
#         except Exception as error:
#             print(error)
