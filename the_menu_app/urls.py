from django.urls import path

from .views import DisplayTheEntireSite

urlpatterns = [
    path('', DisplayTheEntireSite.as_view()),
]
