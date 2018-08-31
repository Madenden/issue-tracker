from django.conf.urls import url
from .views import tickets, create_ticket, create_feature

urlpatterns = [
    url(r'^create-feature/', create_feature, name='create-feature'),
    url(r'^create-ticket/', create_ticket, name='create-ticket'),
    url(r'^tickets/', tickets, name='tickets'),
    ]