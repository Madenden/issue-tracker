from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from model_utils.fields import StatusField, MonitorField
from model_utils import Choices


# Create your models here.
class Ticket(models.Model):
    author = models.ForeignKey(User, default=1)
    title = models.CharField(max_length=254, default="")
    description = models.TextField()
    # created_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="bug_upvotes")
    
    STATUS  = Choices('to do', 'doing', 'done')
    status = StatusField()
    status_changed = MonitorField(monitor='status')
    
    ISSUE_STATUS = Choices('bug', 'feature')
    issue_status = StatusField(choices_name='ISSUE_STATUS')
    status_changed = MonitorField(monitor='issue_status')
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="comments")
    author = models.ForeignKey(User)
    content = models.TextField('Comment')
    pub_date = models.DateTimeField('Date of comment', default=timezone.now)

    def __str__(self):
        return self.content