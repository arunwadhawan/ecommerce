from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout

User = get_user_model()

# Create your views here.
def register(request):
    title="Register"
    form = UserCreationForm()
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            name=form.cleaned_data['name']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password1']

            user = User.objects.create_user(email, name, phone_number, password)
            user.save()
            messages.info(request,'User created successfully')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {'title':title, 'form':form,}
    return render(request,'accounts/register.html',context)

def user_login(request):# don't use login as it conflicts with the login import from auth
    title="Login"
    if request.method=='POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email,password=password)
        print(user)

        if user is not None:
            login(request, user)
            #messages.success(request,'You are now logged in.')
            return redirect('store')
        else:
            messages.error(request,'Invalid login credentials.')
            return redirect('login')
    else:
        context = {'title':title}
        return render(request,'accounts/login.html',context)

def user_logout(request): # don't use logout as it conflicts with the logout imported from auth
    title="Login"
    logout(request)
    context = {'title':title}
    return redirect('login')
