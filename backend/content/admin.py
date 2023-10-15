from django.contrib import admin
from django.utils.safestring import mark_safe

from backend.settings import MAX_LEN_TEXT_IN_ADMIN
from .models import Feedback, News, PlatformAbout, Valuation, City


admin.site.site_title = 'Админка BETTER-TOGETHER'
admin.site.site_header = 'Администрирование сайта BETTER-TOGETHER'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'phone',
        'email',
        'get_text',
        'created_at',
        'processed_at',
        'status',
    )
    readonly_fields = ('name', 'phone', 'email', 'text', 'created_at')
    list_filter = ('created_at', 'processed_at', 'status')
    search_fields = ('phone', 'email', 'text')
    ordering = ('status', 'created_at')
    date_hierarchy = 'created_at'
    save_on_top = True

    @admin.display(description='Текст новости сокращенный')
    def get_text(self, obj):
        if obj.text:
            return obj.text[:MAX_LEN_TEXT_IN_ADMIN]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'get_text',
        'created_at',
        'author',
        'get_mini_picture',
        'get_tags',
    )
    readonly_fields = ('created_at', 'author')
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

    @admin.display(description='ТЕГИ')
    def get_tags(self, obj):
        if obj.tags:
            return ', '.join([tag.name for tag in obj.tags.all()])


@admin.register(PlatformAbout)
class PlatformAboutAdmin(admin.ModelAdmin):
    list_display = ('about_us', 'platform_email')


@admin.register(Valuation)
class Valuation(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description')
    ordering = ('-id',)


@admin.register(City)
class City(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-id',)
