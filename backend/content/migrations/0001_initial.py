import content.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, validators=[content.validators.NameFeedbackUserValidator.validate_name], verbose_name='Имя')),
                ('phone', models.CharField(max_length=12, validators=[content.validators.PhoneValidator.validate_phone], verbose_name='Телефон')),
                ('email', models.EmailField(max_length=256)),
                ('text', models.CharField(max_length=750, validators=[content.validators.TextFeedbackValidator.validate_text], verbose_name='Текст обращения')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время обращения')),
                ('processed_at', models.DateTimeField(blank=True, null=True, verbose_name='Дата и время обработки')),
                ('status', models.BooleanField(default=False, verbose_name='Обработано')),
            ],
            options={
                'verbose_name': 'Обращение',
                'verbose_name_plural': 'Обращения',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='PlatformAbout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_us', models.TextField(verbose_name='Описание раздела "О нас"')),
                ('platform_email', models.EmailField(max_length=256, verbose_name='email Платформы')),
            ],
            options={
                'verbose_name': 'О платформе',
                'verbose_name_plural': 'О платформе',
            },
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Навык')),
            ],
            options={
                'verbose_name': 'Навык',
                'verbose_name_plural': 'Навыки',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Valuation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание ценности')),
            ],
            options={
                'verbose_name': 'Ценность платформы',
                'verbose_name_plural': 'Ценности платформы',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, upload_to='news/%Y/%m/%d/')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст новости')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news', to=settings.AUTH_USER_MODEL, verbose_name='Автор новостей')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name': 'Новость',
                'verbose_name_plural': 'Новости',
                'ordering': ('-created_at',),
            },
        ),
    ]
