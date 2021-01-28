from django.urls import path
from django.urls.resolvers import URLPattern 
from app1.views import home

urlpatterns = [
    path('', home, name='home'),
]
