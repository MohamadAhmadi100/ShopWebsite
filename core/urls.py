from django.urls import path, re_path
from .views import home

app_name = 'core'

urlpatterns = [
    path('', home, name='home')
]
