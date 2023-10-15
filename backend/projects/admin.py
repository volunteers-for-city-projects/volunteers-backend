from django.contrib.admin import ModelAdmin, register

from projects.models import Category, Organization, Project, Volunteer


@register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = (
        'contact_person',
        'title',
        'ogrn',
        'phone',
        'about',
        'city',
    )
    search_fields = (
        'title',
        'ogrn',
        'phone',
    )
    list_filter = (
        'title',
        'city',
    )
    save_on_top = True
    empty_value_display = '-пусто-'


@register(Volunteer)
class VolunteerAdmin(ModelAdmin):
    list_display = (
        'user',
        'city',
        'telegram',
        'skills',
        'photo',
        # 'activities',
        'date_of_birth',
        'phone',
    )
    search_fields = (
        'telegram',
        'phone',
    )
    list_filter = (
        'city',
        'skills',
    )
    save_on_top = True
    empty_value_display = '-пусто-'


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    search_fields = (
        'name',
        'slug',
    )
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    save_on_top = True


@register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = (
        'name',
        'description',
        'picture',
        'start_datatime',
        'end_datatime',
        'application_date',
        'event_purpose',
        'organization',
        'city',
        'category',
        'photo_previous_event',
        'participants',
        'status_approve',
    )
    search_fields = (
        'name',
        'start_datatime',
        'organization',
        'city',
        'category',
    )
    list_filter = (
        'start_datatime',
        'organization',
        'city',
        'category',
        'status_approve',
    )
    save_on_top = True
    empty_value_display = '-пусто-'
