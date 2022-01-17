from django.db import models
from django.contrib.auth.models import User, UserManager
import datetime
# Create your models here.

    
class company(models.Model):
    companyname=models.CharField(max_length=255)
    branchcode=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    username=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username')
    def __str__(self):
        return self.companyname


class fuel(models.Model):
    fuelname=models.CharField(max_length=255)
    quantity=models.IntegerField(blank=False)
    date=models.DateField(default=datetime.date.today())
    sellPrice=models.IntegerField(blank=False)
    buyingPrice=models.IntegerField(blank=False)
    username=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username')

    def __str__(self):
        return self.fuelname +"-"+str(self.date)

class tank(models.Model):
    fuelname=models.CharField(max_length=255)
    totalquantity=models.IntegerField(blank=False)
    username=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username')
    def __str__(self):
        return self.fuelname

# DELETE AFTER

class Item(models.Model):
    itemName=models.CharField(max_length=255)
    itemDesc=models.CharField(max_length=255)
    sellPrice=models.IntegerField(blank=False)
    quantity=models.IntegerField(blank=False)
    username=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username')
    Category=models.CharField(max_length=255,default="null")

    def __str__(self):
        return self.itemName

class record(models.Model):
    fuelname=models.CharField(max_length=255,default="")
    # fuelname=models.CharField(max_length=255,blank=False)
    cname=models.CharField(max_length=255)
    phonenumber=models.IntegerField(blank=False,default="NULL")
    quantity=models.IntegerField(blank=False)
    platenumber=models.CharField(max_length=255,default="")
    amount =models.IntegerField(blank=False)
    username=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username',default="")

    # def __str__(self):
    #     return self.customername

#'itemId','fuelname','customername','phonenumber','quantity','platenumber','amount')

class customer(models.Model):
    fuelname=models.CharField(max_length=255)
    customername=models.CharField(max_length=255,default="")
    phone=models.IntegerField(blank=False)
    platenumber = models.CharField(max_length=255)
    quantity=models.IntegerField(blank=False)
    amount=models.IntegerField(blank=False)
    username=models.ForeignKey(User,on_delete=models.CASCADE,to_field='username')
    
