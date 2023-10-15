from django.urls import include, path
from rest_framework.routers import DefaultRouter


from .views import (
    NewsViewSet,
    PlatformAboutView,
    FeedbackCreateView,
    ProjectViewSet,
)


router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'projects', ProjectViewSet, basename='projects')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),  # это вроде можно убрать
    path('auth/', include('djoser.urls.authtoken')),
    path('platform_about/', PlatformAboutView.as_view()),
    path('feedback/', FeedbackCreateView.as_view()),
]
