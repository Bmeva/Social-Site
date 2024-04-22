from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Profile, User
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout
# Create your views here.


def Register5(request): # I defined a signal which creates the Profile immedieatly a user is created
    """
    if request.user.is_authenticated:
        messages.info(request, 'You are already registered')
        return redirect('index')
    """
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        full_name = form.cleaned_data.get('full_name')
        phone = form.cleaned_data.get('phone')
        email = form.cleaned_data.get('email')
        password1 = form.cleaned_data.get('password1')

        user = authenticate(email=email, password= password1)
        login(request, user)

        messages.success(request, f"Hi  {full_name}. Your account has been created succesfully")

        #if you use django signals to create the profile immdiately user has been created you can 
        #use this code below to create some fields in the profile
        profile = Profile.objects.get(user = request.user)
        profile.full_name = full_name
        profile.phone = phone
        profile.city = email
        profile.save()

        return redirect('index')

    context = {
        'form': form,
    }
    return render(request, 'Authentication/signup.html', context)


def mylogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are Logged In")
                return redirect('index')
            else:
                messages.error(request, 'Username or password does not exit.')
        
        except:
            messages.error(request, 'User does not exist')

    return render(request, 'Authentication/signup.html')
    
          



#this can be used to create a profile directly if i did not use django signals
def Register(request):

        
    if request.user.is_authenticated:
        messages.info(request, 'You are already registered')
        return redirect('index')
    
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        full_name = form.cleaned_data.get('full_name')
        phone = form.cleaned_data.get('phone')
        email = form.cleaned_data.get('email')
        password1 = form.cleaned_data.get('password1')

        if User.objects.filter(email=email).exists(): #this is not even neccesary becouse on the model we said email should be unique
        
            messages.error(request, "account already exist")
        else:
            user.save()
        # #afrer the account i dont want to leave the user profile completely empty so i want to add a
        #few data to it
            profile = Profile.objects.create(

                user=user,  # Associate the profile with the newly created user
                full_name=full_name,
                phone=phone,
                city=email
            )
            profile.save()

            user = authenticate(request, email=email, password= password1)
            login(request, user)

            messages.success(request, f"Hi  {full_name}. Your account has been created succesfully")
        
        
            return redirect('index')

    context = {
        'form': form,
    }
    return render(request, 'Authentication/signup.html', context)



def mylogout(request):
    logout(request)
    messages.info(request, 'You are now logged out')
    return redirect('Register')



