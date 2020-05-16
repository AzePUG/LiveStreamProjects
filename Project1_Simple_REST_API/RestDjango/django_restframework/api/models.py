from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Todo(models.Model):
    user = models.ForeignKey(User, models.SET_NULL,blank=True,null=True)
    title = models.CharField(max_length=50,null=False,blank=False)
    description = models.CharField(max_length=250,null=False,blank=False)


    def __str__(self):
        return f'{self.title}'

    
