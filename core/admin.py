from django.contrib import admin

from .models import PostMessage , comment

# Register your models here.
admin.site.register(PostMessage)
admin.site.register(comment)