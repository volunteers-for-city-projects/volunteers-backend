from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title='BETTER-TOGETHER Documentation API')
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    #  логин в джанго свагер Проверить никому не помешает ли!!!
    path('accounts/login/', LoginView.as_view(
        template_name='admin/login.html',
    )),
    # логаут в джанго свагер. Проверить никому не помешает ли!!!
    path('accounts/logout/', LogoutView.as_view(
        template_name='admin/logout.html',
    )),
    # path('swagger/', schema_view),
]

urlpatterns += doc_urls

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
