from django.contrib.auth.models import User
from django.db import models

# Create your models here.
User._meta.get_field('email')._unique = True

class PostMessage(models.Model):
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    image = models.ImageField(upload_to="core/images",default="",null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username + " " + self.content[:20]

    class Meta:
        ordering = ('date_added',)


class comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    message = models.ForeignKey(PostMessage,related_name='message',on_delete=models.CASCADE)
    content = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return  self.user.username + " " + self.content[:20]

    class Meta:
        ordering = ('-date_added',)