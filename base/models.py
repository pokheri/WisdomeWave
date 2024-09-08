from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# Here we creating the database table using the python classes : 


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    


class Room(models.Model):
    # if the Topic  is defined after the 'Room' we can still use the room, using string specification : like this 'Room' 
    host = models.ForeignKey(User, on_delete= models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # adding  the participants , and it will be the many  to many fields 
    participants = models.ManyToManyField(User,related_name='participants' , null=True)
    updated = models.DateTimeField(auto_now=True)
    created  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.name
    

class Message(models.Model):

    # one to many relationship 
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created  = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.body[0:40]
    
    
    class Meta:
        ordering = ['-updated', '-created']
