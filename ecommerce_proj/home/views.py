from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from home.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect

def home(request):
    return render(request, 'home/index.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request,"Passwords do not match")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email already exists")
            return redirect('register')

        
        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email, 
                password=password
            )
            messages.success(request,"User created successfully")
            print('hello')
            user.generate_verification_code()

            request.session['email'] = email

            return redirect('otp_verification')
        except Exception as e:
            print('hi')
            messages.error(request,f"Error creating user:{e}")
            return redirect('register')

    return render(request, 'account/register.html')

def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,"Invalid email or password")
            return redirect('login')
    
    return render(request, 'account/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')

def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email')
        if not email:
            messages.error(request, "Session expired. Please register again.")
            return redirect('register')
        try:
            user = User.objects.get(email=email)
            if user.verify_otp(otp):
                user.is_verified = True
                user.is_active = True
                user.save()
                messages.success(request, "User verified successfully")
                return redirect('login')
            else:
                messages.error(request, "Invalid OTP")
                return redirect('otp_verification')
        except ObjectDoesNotExist:
            messages.error(request, "User does not exist. Please register again.")
            return redirect('register')


    return render(request, 'account/otp.html')
