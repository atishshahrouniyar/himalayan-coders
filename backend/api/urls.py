from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentProfileViewSet, ProfessorProfileViewSet, 
    MatchViewSet, SearchViewSet
)

router = DefaultRouter()
router.register(r'students', StudentProfileViewSet)
router.register(r'professors', ProfessorProfileViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'search', SearchViewSet, basename='search')

urlpatterns = [
    path('', include(router.urls)),
]
