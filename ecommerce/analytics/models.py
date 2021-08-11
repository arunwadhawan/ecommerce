from django.conf import settings # to import the User from settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
#from django.contrib.auth.models import User - Not reqd as custom user model beng used
from django.db import models
from .signals import object_viewed_signal
from .utils import get_client_ip


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
    
    

