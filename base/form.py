from django.forms import ModelForm
from django import forms
from base.models import Room, Message
from django.contrib.auth.models import User

class RoomFrom(ModelForm):

    class Meta:
        model = Room
        # this  will give all the list : 
        fields = '__all__'
        exclude = ['host', 'participants']
        


class MessageForm(ModelForm):

    class Meta:
        model = Message
        fields = '__all__'




class UserForm(ModelForm):
    
 
    class Meta:
        model = User
        fields = ['username', 'email' ]