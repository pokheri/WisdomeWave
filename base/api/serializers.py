from rest_framework.serializers import ModelSerializer
from base.models import Room
from django.contrib.auth.models import User





# this is the serializer class for converting the simple object , into json formate or json ccepted formate : 




class RoomSerailizer(ModelSerializer):
    
    class Meta:
        model = Room
        fields = '__all__'


class UserSerialize(ModelSerializer):
    class Meta:
    

        model = User
        fields = ['username', 'email']
