from django.shortcuts import render
# lookup method : for multiple value in serach bar : , depdending on the base value in dynamic: 
from django.db.models import Q
from django.http import HttpResponse
# Create your views here.
from base.models import Room, Topic
from base.form import RoomFrom, UserForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from base.models import Message



from base.form import MessageForm

def loginPage(request):
    page = 'login'
    # restricting user to login again , if they are login : 
    if request.user.is_authenticated:
        return HttpResponse('you are already login : ')
    

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            # getting the user 
            user = User.objects.get(username = username)

        except :
            messages.error(request, 'The user is not exits in the Registeration : ')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user=user)
            return redirect('home')
        else:
            messages.info(request,'username and password does not exits :')
        
    return render(request, 'base/regi_login.html',{'page':page})


def logoutPage(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # automatically login the user , in the website : 
            login(request, user)
            return redirect('home')
        else: 
            messages.error(request, 'The Form is invalid : ')
            return redirect('register_user')
        
    return render(request, 'base/regi_login.html', {'page': page, 'form': form})



def home(request):  
    room = Room.objects.all()
    topic  = Topic.objects.all()
    room_count = room.count()
    q  = request.GET.get('q') if request.GET.get('q') else ''
    room = Room.objects.filter(Q(topic__name__icontains = q)
                               | Q(name__icontains=q) 
                               | Q(description__icontains=q  ))

    

    room_messages = Message.objects.filter(Q(room__name__icontains =q),
                                           Q(room__topic__name__icontains =q))
    

    context = {
        'rooms': room[0:3],
        'topics': topic[:9],
        'room_count': room_count,
        'room_messages': room_messages[0:3],
    





    }
    
    return render(request, 'base/home.html',context )



def room(request, pk ):
    
    room =Room.objects.get(pk = int(pk) )
    # we can query up to the the childe model like this : 
    # messages = room.message_set.all(), message is model name 
    # --- or we can use the relative name attribute specify in the model 
    messages = room.messages.all().order_by('-created')
    # accesing the participants 
    participants = room.participants.all()

    if request.method == 'POST':
     message = Message.objects.create(
         user = request.user,
         room = room,
         body = request.POST.get('body') 
     )
     # this is the way we can add the user in the participants list :
     room.participants.add(request.user)
     
     return redirect('room' , pk=room.id )
    


    context = {
        'room': room, 
        'room_messages': messages, 
        'participants':  participants,


    }

    return render(request, 'base/room.html', context)


def userProfile(request,pk):
    user = User.objects.get(pk = int(pk))


    # message =Message.objects.filter(user = user )
    message  = user.message_set.all()
    topics = Topic.objects.all()
    room_count = Room.objects.filter(host = user).count()
    print('the value of the count',room_count)

    q  = request.GET.get('q') if request.GET.get('q') else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q)
                               | Q(name__icontains=q) 
                               | Q(description__icontains=q  )).filter(host = user)
    

    message = Message.objects.filter(Q(room__name__icontains =q),
                                           Q(room__topic__name__icontains =q)).filter(user = user )
    
 


    context = {
        'user': user,
        'rooms': rooms,
        'room_messages': message , 
        'topics': topics, 
        'room_count': room_count, 
        'next': 'profile',
        



    }
    return render(request, 'base/profile.html', context )


@login_required
def updateUser(request ):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form  = UserForm(request.POST, instance=user)
        if form.is_valid():
          
            user.save()

            return redirect('user-profile', user.id)
        else: 
            messages.info(request, 'the data is wrong ')
            return redirect('update-user')
    

    context ={
        'form': form, 

        
    }
    return render(request, 'base/update_user.html', context )







@login_required
def createRoom(request):
    room = RoomFrom()
    topics = Topic.objects.all()

    if request.method == "POST":
        topic_name = request.POST.get('topic')  
        # the use of the get or create 
        topic, created  = Topic.objects.get_or_create(name=topic_name)

        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            
        )
        print('yeah')
        return redirect('home')
        
        
    context ={
        'form': room,
        'topics': topics,
        
    }
    return render(request, 'base/room_form.html', context)

@login_required
def updateRoom(request, pk ):
    room =Room.objects.get(pk = pk )
    # The initial instance for the predefined data in the form : 
    form = RoomFrom(instance=room)
    topics = Topic.objects.all()

    if request.user!= room.host:
        return HttpResponse(f'Hey {request.user} . You are not allowed to do that , becuase its "{room.host}" room ')
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')  
        # the use of the get or create 
        topic, created  = Topic.objects.get_or_create(name=topic_name)


        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
     



    
    context = {
        'form': form, 
        'topics': topics,
        'room':room, 
        


    }
    return render(request, 'base/room_form.html', context)
@login_required
def deleteRoom(request, pk ):
    room = Room.objects.get(pk=pk)
    if request.user!= room.host:
        return HttpResponse(f'Hey {request.user} . You are not allowed to do that , becuase its "{room.host}" room ')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html' , {'obj': room})


# deleting the message : 
@login_required
def deleteMessge(request,pk):
    message = Message.objects.get(pk=pk)
    if request.user!= message.user:
        return HttpResponse(f'Hey {request.user} . You are not allowed to do that , becuase its "{message.user}" room ')
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html' , {'obj': message})



def browseTopics(request):
    
    room_count = Room.objects.all().count()

    q = request.GET.get('q') if request.GET.get('q') else ''
    if q:
        topics = Topic.objects.filter(name__icontains =q)

    else:
        topics  = Topic.objects.all()[0:5]



    context = {
        'topics': topics,
        'room_count': room_count

    }
    
    return render(request, 'base/topics.html', context )



def recentActivity(request):
    activites = Message.objects.all().order_by('-pk')

    context = {
        'activites': activites[:3] 

    }
    
    return render(request, 'base/activity.html', context )