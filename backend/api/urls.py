from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from api.views import (
    CityViewSet,
    FeedbackCreateView,
    NewsViewSet,
    OrganizationViewSet,
    PlatformAboutView,
    ProjectCategoryViewSet,
    ProjectViewSet,
    SearchListView,
    SkillsViewSet,
    TagViewSet,
    VolunteerProfileView,
    VolunteerViewSet,
)

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'project_categories', ProjectCategoryViewSet)
router.register(r'volunteers', VolunteerViewSet, basename='volunteers')
router.register(
    r'organizations', OrganizationViewSet, basename='organizations'
)
router.register(r'cities', CityViewSet)
router.register(r'skills', SkillsViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/me/', UserViewSet.as_view({'get': 'me'}),),
    path('auth/change_password/',
         UserViewSet.as_view({'post': 'set_password'}),
         name='set_password'),
    path('auth/reset_password/',
         UserViewSet.as_view({'post': 'reset_password'}),
         name='password_reset'),
    path('auth/', include('djoser.urls.authtoken')),
    path('platform_about/', PlatformAboutView.as_view()),
    path('feedback/', FeedbackCreateView.as_view()),
    path('search/', SearchListView.as_view()),
    path('volunteers/profile/<int:pk>/', VolunteerProfileView.as_view()),
]
