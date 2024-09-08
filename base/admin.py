from django.contrib import admin

# Register your models here.
from base.models import Room, Topic, Message

@admin.register(Room)
class RoomAdminModel(admin.ModelAdmin):
    list_display  = ['name', 'description','created', 'updated']
    list_filter =['name', 'created', 'updated']

# we have registered this to the admin , so we can manupluate them : 

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name']




@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display  = ['body', 'room', 'user']


    