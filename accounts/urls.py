from django.urls import path
from django.contrib.auth.views import LogoutView

app_name = 'accounts'
urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]
