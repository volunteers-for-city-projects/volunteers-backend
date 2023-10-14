from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NewsViewSet, PlatformAboutView, FeedbackCreateView


router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('platform_about/', PlatformAboutView.as_view()),
    path('feedback/', FeedbackCreateView.as_view()),

]
