from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='BETTER-TOGETHER Documentation API')

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
