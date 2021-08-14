from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from .signals import user_logged_in
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
#Email enablement imports
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string #converts the html template to text for embedding into email body
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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
            
##            #User activation - to activate sert the is_active to False in the User Model
##            current_site=get_current_site(request)
##            mail_subject = 'Please activaye your account by clicking on this link'
##            message = render_to_string('accounts/account_verification_email.html',{
##                'user':user,
##                'domain':current_site,
##                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
##                'token':default_token_generator.make_token(user),
##                })
##            to_email = email
##            send_email = EmailMessage(mail_subject, message,to=[to_email])
##            send_email.send()
            
            messages.info(request,'User created successfully')
            return redirect('login')
    else:
        form = UserCreationForm()
    context = {'title':title, 'form':form,}
    return render(request,'accounts/register.html',context)

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and defaut_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        message.success(request,'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')
    
    
def user_login(request):# don't use login as it conflicts
    title="Login"
    if request.method=='POST':
        
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email,password=password)
        if user is not None:
            login(request, user)
            print(user)
            user_logged_in.send(user.__class__, instance=user,request=request)
            #messages.success(request,'You are now logged in.')
            return redirect('store')
        else:
            messages.error(request,'Invalid login credentials.')
            return redirect('login')
    else:
        context = {'title':title}
        return render(request,'accounts/login.html',context)

@login_required(login_url='login')
def user_logout(request): # don't use logout as it conflicts with the logout imported from auth
    title="Login"
    logout(request)
    context = {'title':title}
    return redirect('login')
