from django.contrib.admin import ModelAdmin, register

from projects.models import Organization, Volunteer, Project


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


@register(Volunteer)
class VolunteerAdmin(ModelAdmin):
    list_display = (
        'user',
        'city',
        'telegram',
        'skills',
        'photo',
        'activites',
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
