from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from model_utils.fields import StatusField, MonitorField
from model_utils import Choices


# Create your models here.
class Ticket(models.Model):
    author = models.ForeignKey(User, default=None)
    title = models.CharField(max_length=254, default="")
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    STATUS  = Choices('to do', 'doing', 'done')
    status = StatusField()
    status_changed = MonitorField(monitor='status')
    
    
    def __str__(self):
        return self.title
        
    def snippet(self):
        return self.description[:150] + "..."