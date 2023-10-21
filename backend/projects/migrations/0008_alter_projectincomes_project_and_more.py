# Generated by Django 4.2.6 on 2023-10-20 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_projectincomes_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectincomes',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_incomes', to='projects.project', verbose_name='Проект'),
        ),
        migrations.AlterField(
            model_name='projectincomes',
            name='status_incomes',
            field=models.CharField(blank=True, choices=[('application_submitted', 'Заявка подана'), ('rejected', 'Отклонена'), ('accepted', 'Принята')], default=None, null=True, verbose_name='Статус заявки волонтера'),
        ),
        migrations.AlterField(
            model_name='projectincomes',
            name='volunteer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_incomes', to='projects.volunteer', verbose_name='Волонтер'),
        ),
        migrations.AddConstraint(
            model_name='projectincomes',
            constraint=models.UniqueConstraint(fields=('project', 'volunteer', 'status_incomes'), name='projectsprojectincomes_unique_project_volunteer'),
        ),
    ]