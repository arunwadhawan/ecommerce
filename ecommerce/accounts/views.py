from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages

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

def login(request):
    title="Login"
    context = {'title':title}
    return render(request,'accounts/login.html',context)

def logout(request):
    title="Logout"
    context = {'title':title}
    return render(request,'accounts/register.html',context)
