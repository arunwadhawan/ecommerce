from django.conf import settings
from django.urls import reverse
from django.db import models
#from django.contrib.auth.models import User - Not reqd as custom user model beng used
from django.db.models.signals import pre_save
from .utils import unique_slug_generator
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    #date_created = models.DateTimeField(auto_now_add=True,blank=True, default=datetime.now)
    #date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=255, null=True, blank=False)
    image = models.ImageField(upload_to='categories', blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    #date_created = models.DateTimeField(auto_now_add=True,blank=True)
    #date_modified = models.DateTimeField(auto_now=True)
        
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name

# to be used to filter products by categories
    def get_absolute_url(self):
        return reverse('products_by_category',args=[self.slug])

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    description = models.TextField(max_length=500, null=True, blank=False)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    images = models.ImageField(upload_to='products', blank=True)
    stock = models.IntegerField(null=True, blank=False)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    #date_created = models.DateTimeField(auto_now_add=True,blank=True, default=datetime.now)
    #date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args =[self.category.slug,self.slug])

    @property
    def imageURL(self):
        try:
            url = self.images.url
        except:
            url = ''
        return url
    
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)
        
pre_save.connect(product_pre_save_receiver, sender=Product)
        
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True,blank=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping=False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)
    #date_added = models.DateTimeField(auto_now_add=True,blank=True, default=datetime.now)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        total = self.quantity * self.product.price
        return total
        
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True, default="India")
    pincode = models.CharField(max_length=200, null=True)
    #date_added = models.DateTimeField(auto_now_add=True,blank=True, default=datetime.now)
    #date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)

    
