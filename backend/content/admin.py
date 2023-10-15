from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils import timezone

from backend.settings import MAX_LEN_TEXT_IN_ADMIN
from .models import Feedback, News, PlatformAbout, Valuation, City


admin.site.site_title = 'Админка BETTER-TOGETHER'
admin.site.site_header = 'Администрирование сайта BETTER-TOGETHER'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    '''Администрирование раздела обращений от пользователей.'''

    list_display = (
        'name',
        'phone',
        'email',
        'get_text',
        'created_at',
        'processed_at',
        'status',
    )
    readonly_fields = (
        'name',
        'phone',
        'email',
        'text',
        'created_at',
        'processed_at',
    )
    list_editable = ('status',)
    list_filter = ('created_at', 'processed_at', 'status')
    search_fields = ('phone', 'email', 'text')
    ordering = ('status', 'created_at')
    date_hierarchy = 'created_at'
    save_on_top = True

    @admin.display(description='Текст новости сокращенный')
    def get_text(self, obj):
        if obj.text:
            return obj.text[:MAX_LEN_TEXT_IN_ADMIN]

    def save_model(self, request, obj, form, change):
        if obj.status:
            obj.processed_at = timezone.now()
        else:
            obj.processed_at = None
        super().save_model(request, obj, form, change)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):

    '''Администрирование раздела новостей.'''

    list_display = (
        'title',
        'get_text',
        'created_at',
        'author_initials',
        'get_mini_picture',
        'get_tags',
    )
    readonly_fields = ('created_at',)
    list_filter = ('title', 'created_at', 'author', 'tags')
    search_fields = ('title', 'text', 'tags')
    ordering = ('created_at',)
    date_hierarchy = 'created_at'
    save_on_top = True

    @admin.display(description='Картинка')
    def get_mini_picture(self, obj):
        if obj.picture:
            return mark_safe(f"<img src='{obj.picture.url}' width=50>")

    @admin.display(description='Текст новости сокращенный')
    def get_text(self, obj):
        if obj.text:
            return obj.text[:MAX_LEN_TEXT_IN_ADMIN]

    @admin.display(description='Автор новости')
    def author_initials(self, obj):
        if obj.author:
            last_name = obj.author.last_name
            first_initial = (
                obj.author.first_name[0] if obj.author.first_name else ''
            )
            second_initial = (
                obj.author.second_name[0] if obj.author.second_name else ''
            )
            return f"{last_name} {first_initial}.{second_initial}."

    @admin.display(description='ТЕГИ')
    def get_tags(self, obj):
        if obj.tags:
            return ', '.join([tag.name for tag in obj.tags.all()])


@admin.register(PlatformAbout)
class PlatformAboutAdmin(admin.ModelAdmin):
    '''Администрирование раздела О Платформе'''

    list_display = ('about_us', 'platform_email')


@admin.register(Valuation)
class Valuation(admin.ModelAdmin):
    '''Администрирование раздела Ценности Платформы.'''

    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    ordering = ('-id',)


@admin.register(City)
class City(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-id',)
