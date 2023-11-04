import os
from csv import DictReader

from django.core.management.base import BaseCommand

from content.models import City, News, Skills, Valuation
from projects.models import (
    Address,
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
    Address: 'address.csv',
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
