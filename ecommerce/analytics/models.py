from django.conf import settings # to import the User from settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth.models import User - Not reqd as custom user model beng used
from django.contrib.sessions.models import Session
from django.db import models
from django.db.models.signals import pre_save, post_save
from .signals import object_viewed_signal
from .utils import get_client_ip
from accounts.signals import user_logged_in

#Import the session based settings from the settings file
FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE',False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION',False)
# Create your models here.

User = settings.AUTH_USER_MODEL # helps import the user model whether custom or standard

class ObjectViewed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True,null=True)
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s viewed on %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp'] # Most recent saved show up first
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'

def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender) # get the model
    print(sender)
    print(instance)
    print(request.GET)
    print(request.user)
    new_view_obj = ObjectViewed.objects.create(
        user = request.user,
        ip_address = get_client_ip(request),
        content_type = c_type,
        object_id = instance.id,
        
        )

object_viewed_signal.connect(object_viewed_receiver)


class UserSession(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=True,null=True)
    ip_address = models.CharField(max_length=220, blank=True, null=True)
    session_key = models.CharField(max_length=100,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False) # if it was ended manually


    def end_session(self):
        session_key = self.session_key
        try:
            Session.objects.get(pk=session_key).delete()
            self.active=False
            print(self.active)
            self.ended = True
            print(self.ended)
            self.save()
        except:
            pass
        return self.ended

def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        
        qs = UserSession.objects.filter(user=instance.user,ended=False).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()

if FORCE_SESSION_TO_ONE: # Configuration maintained in settings file
    post_save.connect(post_save_session_receiver,sender=UserSession)

#End all the sessions, if the session is terminated manually....including the latest one
def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    print("Signal red: Post save user", instance.email, instance)
    if not created:
        if instance.is_active == False:
            qs = UserSession.objects.filter(user=instance,ended=False,active=True)
            
            for i in qs:
                i.end_session()

if FORCE_INACTIVE_USER_ENDSESSION: #Config maintained in the settings file
    post_save.connect(post_save_user_changed_receiver,sender=User)



def user_logged_in_receiver(sender, instance, request,*args,**kwargs):
    print("Signal red: user_logged_in", instance, instance) 
    user = instance
    ip_address = get_client_ip(request)
    session_key = request.session.session_key
    UserSession.objects.create(user=user,ip_address=ip_address, session_key=session_key)
      
user_logged_in.connect(user_logged_in_receiver)
    
    

