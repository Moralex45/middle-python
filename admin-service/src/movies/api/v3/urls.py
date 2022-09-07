"""config URL Configuration."""
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'', views.MoviesViewSet, basename='filmwork')

print(router.urls)

urlpatterns = [
    path('movies/', include(router.urls)),
]
