from django.conf.urls import url
from .views import alarm_clock

urlpatterns = [
    url(r'^$', alarm_clock, name='alarm_clock'),
    ]