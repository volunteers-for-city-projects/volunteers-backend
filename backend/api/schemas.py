from drf_yasg import openapi

#  параметры натройки для свагера, фильтр проектов в ЛК
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
        description=('Фильтрует проекты организатора/волонтера в архиве'
                     '(отменненые организатором). '
                     'Пример запроса /projects/me/?archive=true')
    ),
    openapi.Parameter(
        'moderation', openapi.IN_QUERY, type=openapi.TYPE_STRING,
        description=('Фильтрует проекты организатора на модерации. '
                     'Пример запроса /projects/me/?moderation=true')
    ),
    openapi.Parameter(
        'is_favorited', openapi.IN_QUERY, type=openapi.TYPE_STRING,
        description=('Фильтрует избранные проекты организатора/волонтера. '
                     'Пример запроса /projects/me/?is_favorited=true')
    ),
]

project_incomes_filter_params = openapi.Parameter(
        'project_id', openapi.IN_QUERY, type=openapi.TYPE_STRING,
        description=('Фильтрует заявки по id проекта. '
                     'Пример запроса /api/incomes/?project_id=1')
    )
