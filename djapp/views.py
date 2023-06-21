from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    return render(request,"authentication/index.html")
def signup(request):

    if request.method == "POST":
        username= request.POST.get('username')
        fname= request.POST.get('fname')
        lname= request.POST.get('lname')
        email= request.POST.get('email')
        pass1= request.POST.get('pass1')
        pass2= request.POST.get('pass2')

        if User.objects.filter(username=username):
            messages.error(request,"username alraedy exists.Please try another Username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request,"Email alraedy exists.")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request,"Username must be under 10 characters")

        if pass1!=pass2:
            messages.error(request,"Password didn't match")

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric!")
            return redirect('home')


        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request,"Your account has been succesfully created")
        return redirect('signin')

    return render(request,"authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username= request.POST.get('username')
        pass1= request.POST.get('pass1')
        user = authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            fname= user.first_name
            return render(request,"authentication/index.html",{'fname':fname})
        else :
            messages.error(request,"Bad Credentials")
            return redirect('home')
    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"You are Logged Out successfully")
    return redirect('home')