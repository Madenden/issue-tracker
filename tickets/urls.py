from django.conf.urls import url
from .views import tickets, the_ticket, create_bug_ticket, create_feature, upvote, ChartData

urlpatterns = [
    url(r'^create-feature/', create_feature, name='create-feature'),
    url(r'^create-bug-ticket/', create_bug_ticket, name='create-bug-ticket'),
    url(r'^tickets/', tickets, name='tickets'),
    url(r'^(?P<pk>\d+)/$', the_ticket, name='the-ticket'),
    url(r'^upvote/(?P<pk>\d+)/$', upvote, name='upvote'),
    url(r'^chart/data/$', ChartData.as_view()),
    ]