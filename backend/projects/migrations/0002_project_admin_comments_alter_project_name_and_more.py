# Generated by Django 4.2.6 on 2023-11-18 00:26

import datetime
import django.core.validators
from django.db import migrations, models
import projects.validators


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='admin_comments',
            field=models.TextField(
                blank=True,
                validators=[
                    projects.validators.regex_string_validator,
                    projects.validators.LengthValidator(
                        max_length=750, min_length=2
                    ),
                ],
                verbose_name='Комментарии администратора',
            ),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(
                max_length=150,
                unique=True,
                validators=[projects.validators.validate_name],
                verbose_name='Название',
            ),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='date_of_birth',
            field=models.DateField(
                help_text='Введите дату в формате "ГГГГ-ММ-ДД", пример: "2000-01-01".',
                validators=[
                    django.core.validators.MinValueValidator(
                        limit_value=datetime.date(1900, 1, 1)
                    ),
                    django.core.validators.MaxValueValidator(
                        limit_value=datetime.date(2023, 11, 18)
                    ),
                ],
                verbose_name='Дата рождения',
            ),
        ),
    ]