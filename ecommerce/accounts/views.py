from django.shortcuts import render
from .forms import RegistrationForm
# Create your views here.

def register(request):
    title="Register"
    form = RegistrationForm()
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
