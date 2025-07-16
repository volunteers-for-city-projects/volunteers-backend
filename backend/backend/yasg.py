from django.urls import path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class HttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    """Add HTTP and HTTPS request type to swagger documentation."""

    def get_schema(self, request=None, public=False):
        """Get schema for swagger."""
        schema = super().get_schema(request, public)
        schema.schemes = ['https', 'http']
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title='BETTER-TOGETHER',
        default_version='v1',
        description="""API documentation for Task BETTER-TOGETHER project.
        Contact us.
        <a href="https://t.me/yunker1" target="_blank">Yurij Pomazkin,</a>\
        <a href="https://t.me/ruzal_z" target="_blank">Ruzal Zakirov,</a>\
        <a href="https://t.me/ArtemKAF" target="_blank">Artem Kozin,</a>\
        <a href="https://t.me/Mirabilis_ignotus" target="_blank">Olga Komleva,\
        </a>\
        and <a href="https://t.me/yourhot" target="_blank">Irina Yablokova
        </a>""",
        contact=openapi.Contact(email="info@bettertogether.ru"),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=HttpAndHttpsSchemaGenerator,
)


urlpatterns = [
    path(
        'swagger<format>/',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    path(
        'swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
