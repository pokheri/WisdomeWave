from django.urls import path
from base import views

#  list of url patterns  : 
urlpatterns = [
    path('login/', views.loginPage, name='login_user'),
    path('logout/', views.logoutPage, name = 'logout_user'),
    path('register/', views.registerPage, name = 'register_user'),
    path('update-user/', views.updateUser, name = 'update-user'),
    
    

    path('', views.home, name = 'home'),
    path('room/<str:pk>/',views.room, name= 'room'),
    path('crate-room/', views.createRoom, name='create-room'),
    path('update-room/<int:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name='delete-room'),

    path('delete-message/<int:pk>/', views.deleteMessge , name = 'delete-message'),
    path('profile/<str:pk>/', views.userProfile, name = 'user-profile'),
    path('browse-topics/', views.browseTopics, name='browse-topics'),
    path('recent-activity/', views.recentActivity, name='recent-activity'),


    # path('user-profile/<int:pk>/', views.userProfile, name = 'userprofile'),


    
    


   


]