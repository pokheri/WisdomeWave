
from django.contrib import admin
from django.urls import path, include





#  This is our project url : 
urlpatterns = [
    path('admin/', admin.site.urls),  
    path('', include('base.urls')),
    path('api/', include('base.api.urls')),
    
    

]
