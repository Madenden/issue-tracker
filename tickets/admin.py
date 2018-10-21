from django.contrib import admin
from .models import Ticket, Comment

# Register your models here.
admin.site.register(Ticket)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'author', 'content')
    
admin.site.register(Comment, CommentAdmin)