from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from api.views import (  # VolunteerProfileView,
    CityViewSet,
    FeedbackCreateView,
    NewsViewSet,
    OrganizationViewSet,
    PlatformAboutView,
    ProjectCategoryViewSet,
    ProjectIncomesViewSet,
    ProjectMeViewSet,
    ProjectViewSet,
    SearchListView,
    SkillsViewSet,
    TagViewSet,
    VolunteerViewSet,
)

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'projects/me', ProjectMeViewSet, basename='my_projects')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'project_categories', ProjectCategoryViewSet)
router.register(r'volunteers', VolunteerViewSet, basename='volunteers')
router.register(
    r'organizations', OrganizationViewSet, basename='organizations'
)
router.register(r'cities', CityViewSet)
router.register(r'skills', SkillsViewSet)
router.register(r'tags', TagViewSet)
router.register(
    r'incomes', ProjectIncomesViewSet, basename='project_incomes'
)

urlpatterns = [
    path('', include(router.urls)),
    path(
        'auth/me/',
        UserViewSet.as_view({'get': 'me'}),
    ),
    path(
        'auth/change_password/',
        UserViewSet.as_view({'post': 'set_password'}),
        name='set_password',
    ),
    path(
        'auth/reset_password/',
        UserViewSet.as_view({'post': 'reset_password'}),
        name='password_reset',
    ),
    path(
        'auth/reset_password_confirm/',
        UserViewSet.as_view({'post': 'reset_password_confirm'}),
        name='password_reset_confirm',
    ),
    path(
        'auth/activation/',
        UserViewSet.as_view({'post': 'activation'}),
        name='activation',
    ),
    path(
        'auth/resend_activation/',
        UserViewSet.as_view({'post': 'resend_activation'}),
        name='resend_activation',
    ),
    path('auth/', include('djoser.urls.authtoken')),
    path('platform_about/', PlatformAboutView.as_view()),
    path('feedback/', FeedbackCreateView.as_view()),
    path('search/', SearchListView.as_view()),
    # path('volunteers/<int:pk>/profile/', VolunteerProfileView.as_view()),
]
