from django.contrib import admin
from .models import BugTicket, FeatureTicket

# Register your models here.
admin.site.register(BugTicket)
admin.site.register(FeatureTicket)