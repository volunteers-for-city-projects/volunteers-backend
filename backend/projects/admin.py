from django.contrib.admin import ModelAdmin, TabularInline, register
from django_object_actions import (
    DjangoObjectActions,
    action,
    takes_instance_or_queryset,
)

from projects.models import (
    Category,
    Organization,
    Project,
    ProjectIncomes,
    ProjectParticipants,
    Volunteer,
    VolunteerSkills,
)


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


class VolunteerSkillsInline(TabularInline):
    model = VolunteerSkills
    verbose_name = 'Навык'
    verbose_name_plural = 'Навыки'


@register(Volunteer)
class VolunteerAdmin(ModelAdmin):
    list_display = (
        'user',
        'city',
        'telegram',
        'photo',
        # 'activities',
        'date_of_birth',
        'phone',
    )
    inlines = (VolunteerSkillsInline,)
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
class ProjectAdmin(DjangoObjectActions, ModelAdmin):
    list_display = (
        'name',
        'description',
        'picture',
        # 'start_datetime',
        # 'end_datetime',
        # 'start_date_application',
        # 'end_date_application',
        # 'event_purpose',
        'organization',
        'city',
        # 'get_categories_display',
        # 'photo_previous_event',
        # 'get_participants_display',
        'status_approve',
        # 'get_skills_display',
    )
    search_fields = (
        'name',
        'start_datetime',
        'description',
        # 'organization',
        # 'city',
        # 'categories',
    )
    list_filter = (
        # 'start_datetime',
        # 'organization',
        # 'city',
        # 'categories',
        'status_approve',
    )
    save_on_top = True
    empty_value_display = '-пусто-'
    ordering = ('id',)

    def get_categories_display(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories_display.short_description = 'Categories'

    def get_skills_display(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])

    get_skills_display.short_description = 'Skills'

    def get_participants_display(self, obj):
        return ", ".join(
            [volunteer.user.last_name for volunteer in obj.participants.all()]
        )

    @action(
        label='Одобрить',
        description='Отправить проект на публикацию',
    )
    def approve_project(self, request, obj):
        obj.status_approve = Project.APPROVED
        obj.save()

    @action(
        label='Отклонить',
        description='Отправить проект на доработку',
    )
    def reject_project(self, request, obj):
        obj.status_approve = Project.REJECTED
        obj.save()

    change_actions = (
        'approve_project',
        'reject_project',
    )

    @action(
        description='Отправить проект на публикацию',
        label='Одобрить',
    )
    @takes_instance_or_queryset
    def approve_projects(self, request, queryset):
        queryset.update(status_approve=Project.APPROVED)

    @action(
        description='Отправить проект на доработку',
        label='Отклонить',
    )
    @takes_instance_or_queryset
    def reject_projects(self, request, queryset):
        queryset.update(status_approve=Project.REJECTED)

    actions = (
        'approve_projects',
        'reject_projects',
    )


@register(ProjectParticipants)
class ProjectParticipantsAdmin(ModelAdmin):
    list_display = (
        'project',
        'volunteer',
    )
    search_fields = (
        'project',
        'volunteer',
    )
    list_filter = ('project',)
    save_on_top = True
    empty_value_display = '-пусто-'


@register(ProjectIncomes)
class ProjectIncomesAdmin(ModelAdmin):
    list_display = (
        'project',
        'volunteer',
        'status_incomes',
        'phone',
        'telegram',
        'cover_letter',
        'created_at',
    )
    search_fields = (
        'name',
        'volunteer',
    )
    list_filter = ('project',)
    save_on_top = True
    empty_value_display = '-пусто-'
