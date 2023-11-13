# Generated by Django 4.2.6 on 2023-11-12 22:07

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_alter_valuation_title'),
        ('projects', '0016_alter_project_options_projectincomes_cover_letter_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='projects', to='projects.category', verbose_name='Категории'),
        ),
        migrations.AlterField(
            model_name='project',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project', to='content.city', verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_date_application',
            field=models.DateTimeField(blank=True, verbose_name='Дата и время, окончания подачи заявок'),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_datetime',
            field=models.DateTimeField(blank=True, verbose_name='Дата и время, окончания мероприятия'),
        ),
        migrations.AlterField(
            model_name='project',
            name='event_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.address', verbose_name='Адрес проведения проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='event_purpose',
            field=models.TextField(blank=True, verbose_name='Цель проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='organizer_provides',
            field=models.TextField(blank=True, verbose_name='Организатор предоставляет'),
        ),
        migrations.AlterField(
            model_name='project',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_events',
            field=models.TextField(blank=True, verbose_name='Мероприятия на проекте'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_tasks',
            field=models.TextField(blank=True, verbose_name='Задачи проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='skills',
            field=models.ManyToManyField(blank=True, related_name='projects', through='projects.ProjectSkills', to='content.skills', verbose_name='Навыки'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date_application',
            field=models.DateTimeField(blank=True, verbose_name='Дата и время, начало подачи заявок'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_datetime',
            field=models.DateTimeField(blank=True, verbose_name='Дата и время, начало мероприятия'),
        ),
        migrations.AlterField(
            model_name='volunteer',
            name='date_of_birth',
            field=models.DateField(help_text='Введите дату в формате "ГГГГ-ММ-ДД", пример: "2000-01-01".', validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(1900, 1, 1)), django.core.validators.MaxValueValidator(limit_value=datetime.date(2023, 11, 12))], verbose_name='Дата рождения'),
        ),
    ]