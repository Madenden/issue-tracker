from django.conf.urls import url
from .forms import MakePaymentForm, TicketForm
from .views import tickets, the_ticket, create_ticket, upvote, ChartData, payment, graphs

urlpatterns = [
    # url(r'^create-feature/', create_feature, name='create-feature'),
    url(r'^create-ticket/', create_ticket, name='create-ticket'),
    url(r'^tickets/', tickets, name='tickets'),
    url(r'^(?P<pk>\d+)/$', the_ticket, name='the-ticket'),
    url(r'^upvote/(?P<pk>\d+)/$', upvote, name='upvote'),
    url(r'^chart/data/$', ChartData.as_view()),
    url(r'^payment/', payment, name='payment'),
    url(r'^graphs/', graphs, name='graphs'),
    ]