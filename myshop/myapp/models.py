from django.db import models
import os
import datetime
from django.contrib.auth.models import User

# Create your models here.

def getfilename(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('images/',new_filename)


class Category(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    category_image=models.ImageField(upload_to=getfilename,null=True,blank=True)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=False,blank=False)
    product_image=models.ImageField(upload_to=getfilename,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    price=models.FloatField(null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_quantity=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

class Orderlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    username=models.CharField(max_length=100,null=False,blank=False)
    phone=models.IntegerField(null=False,blank=False)
    address=models.TextField(max_length=200,blank=False,null=False)
    amount=models.FloatField(blank=False,null=False)
    status=models.CharField(max_length=100,null=False,blank=False)


class Feedback(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    feedback=models.TextField(max_length=250,null=False,blank=False)
    status=models.CharField(max_length=100,null=False,blank=False)

