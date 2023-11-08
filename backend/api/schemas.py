from drf_yasg import openapi


# параметры натройки для свагера, фильтр проектов в ЛК
status_project_filter_params = [
    openapi.Parameter(
        'draft', openapi.IN_QUERY, type=openapi.TYPE_STRING,
        description=('Фильтрует проекты черновики организатора. '
                     'Пример запроса /projects/me/?draft=true')
    ),
    openapi.Parameter(
        'active', openapi.IN_QUERY, type=openapi.TYPE_STRING,
        description=('Фильтрует активные проекты организатора/волонтера. '
                     'Пример запроса /projects/me/?active=true')
    ),
    openapi.Parameter(
        'completed', openapi.IN_QUERY, type=openapi.TYPE_STRING,
        description=('Фильтрует завершенные проекты организатора/волонтера. '
                     'Пример запроса /projects/me/?completed=true')
    ),
    openapi.Parameter(
        'archive', openapi.IN_QUERY, type=openapi.TYPE_STRING,
        description=('Фильтрует проекты организатора в архиве. '
                     'Пример запроса /projects/me/?archive=true')
    ),
]
