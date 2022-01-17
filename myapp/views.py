from datetime import date
from django import forms
from django.contrib.auth import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, UserManager
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib import messages
from myapp.forms import Items, UserForm,company,Fuel,fuel
from random import randrange
from myapp.forms import Item,record,Fuel
from django.conf import settings
from django.core.mail import EmailMessage,send_mail
from .models import *

# import backends.base.SessionBase

# password: lbwrvmmdwscxcgyc


# Create your views here.
# user1=""
def index(request):
    if request.method == "POST":
        uname=request.POST.get("username")
        pwd=request.POST.get("password")
        fname=request.POST.get("first_name")
        lname=request.POST.get("last_name")

        companyname = request.POST.get("companyname")
        branchcode = request.POST.get("branchcode")
        address = request.POST.get("address")
        
        if User.objects.filter(username=uname).exists():
            # print("Existsss")
            messages.error(
            request,
            "User already exists",
            extra_tags="alert alert-error alert-dismissible show",)
            return render(request,'index.html')

        else:
            global temp
            temp = {
            'uname' : uname,
            'pwd' : pwd,
            'fname' : fname,
            'lname' : lname,
            'companyname' : companyname,
            'branchcode' : branchcode,
            'address' : address,
            }        
            otp = randrange(1000,9999)
            subject = otp
            message = f'Hi your otp for Reset password is {otp}.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [uname, ]
            send_mail( subject, message, email_from, recipient_list )
            return render(request,'verify_otp.html',{'otp':otp})
    else:
        return render(request,'index.html')

def signup(request):
    return render(request,"signup.html")

def otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        uotp = request.POST['uotp']
        if otp == uotp:
            global temp
            user = UserForm()
            form = user.save(commit=False)
            form.username = temp["uname"]
            form.first_name = temp["fname"]
            form.last_name = temp["lname"]
            form.set_password(temp["pwd"])
            form.save()
            
            com = company.objects.create(
                username = User.objects.get(username = temp["uname"]),
                companyname = temp["companyname"],
                branchcode = temp["branchcode"],
                address = temp["address"],
            )
            com.save()
                       
            return render(request,'index.html')
    else:
        return render(request,'verify_otp.html')

def auth(request):
    if request.method=="POST":
        
        username = request.POST.get("id")
        password = request.POST.get("pwd")
        user = authenticate(username=username, password=password)
        if user:
            request.session['username']=username
            userf=User.objects.filter(username=username)
            userL=User.objects.all().count()
            comp=company.objects.filter(username=username)
            ptnk=tank.objects.filter(username=username,fuelname='Petrol')
            dtnk=tank.objects.filter(username=username,fuelname='Diesel')
            return render(request, "dashboard.html",{'UC':userL,'userf':userf,'comp':comp,'ptnk':ptnk,'dtnk':dtnk})
        else:
            messages.error(
                request,
                "Account is invalid",
                extra_tags="alert alert-error alert-dismissible show",
            )
            return redirect("index")
    else:
        username=request.session['username']
        userf=User.objects.filter(username=username)
        userL=User.objects.all().count()
        comp=company.objects.filter(username=username)
        ptnk=tank.objects.filter(username=username,fuelname='Petrol')
        dtnk=tank.objects.filter(username=username,fuelname='Diesel')
        return render(request, "dashboard.html",{'UC':userL,'userf':userf,'comp':comp,'ptnk':ptnk,'dtnk':dtnk})

def additems(request):
    if request.method == "POST":
        # print(request.POST)
        # fueldtl=fuel.objects.filter(username=request.POST.get("username"),date=request.POST.get("date"),fuelname=request.POST.get("fuelname"))
        fueldtl=fuel.objects.filter(username=request.POST.get("username"),date=request.POST.get("date"))
        print(fueldtl)
        if fueldtl:
            messages.success(request, "You have already added fuel.If you want to update then go to update page.")
            uid=request.session['username']
            return render(request,"items.html",{'uid':uid})
        if request.POST.get("fuelname")== "Select Fuel":
            messages.success(request, "Please select proper fuel type.")
            uid=request.session['username']
            return render(request,"items.html",{'uid':uid})
        form=Fuel(request.POST) 
        # username = request.POST.get('username')
        # form.fields['username'].choices = [(username, username)]
        if form.is_valid():
            form.save()
            messages.success(request, "Storage has been updated !")
            msg='Storage has been updated successfully !!!'
            uid=request.session['username']
            ufuelname = request.POST.get('fuelname')
            print(ufuelname)
            quantity = request.POST.get('quantity')
            uname=request.session["username"]
            tank1 = tank.objects.get(fuelname=ufuelname,username=uname)
            tank1.totalquantity = tank1.totalquantity + int(quantity)
            tank1.save()
            return render(request,"items.html",{'uid':uid,'msg':msg})
        else:
            print(form.errors)
            return HttpResponse("Invalid!!!!")
    else:
        uid=request.session['username']
        return render(request,"items.html",{'uid':uid})


def updateitems(request):
    uname=request.session['username']
    allIteams = fuel.objects.filter(username=uname)
    cat=fuel.objects.values_list('fuelname',flat=True)
    cat=set(cat)
    context = {'items':allIteams,'category':cat}
    return render(request,"updateitems.html", context)

def edit(request):
    item = Item.objects.all()
    context = {
        'item' : item
    }
    return redirect(request,"updateitems.html")

def update(request):
    if request.method == "POST":
        fuelname = request.POST.get('fuelname')
        date = request.POST.get('date')
        sellprice = request.POST.get('sellPrice')
        buyingprice = request.POST.get('buyingPrice')
        quantity = request.POST.get('quantity')
        tempid = request.POST.get('id')

        fuel1 = fuel.objects.get(id=tempid)
        fuel1.fuelname = fuelname
        fuel1.date = date
        fuel1.sellPrice = sellprice
        fuel1.buyingPrice = buyingprice
        fuel1.quantity = quantity
        fuel1.save()
        return redirect("updateitems")
    return HttpResponse("Error")

def delete(request):
    if request.method == "POST":
        tempid = request.POST.get('id')
        fuel.objects.filter(id=tempid).delete()
        return redirect("updateitems")
    return HttpResponse("Error")

def search(request):
    # if request.method=='POST':
    uname=request.session["username"]
    tanks = tank.objects.filter(username=uname)
    return render(request,'search.html',{"tank":tanks})  
    

# def sell(request,id=0):
#     items=Item.objects.get(pk=id)
#     form=Items(instance=items)
#     return render(request,'search.html',{"form":form})

def sell(request):
    if request.method == "POST":
        uname=request.session["username"]
        ufuelname = request.POST.get('itemName')
        quantity = request.POST.get('quantity')

        tank1 = tank.objects.get(fuelname=ufuelname,username=uname)
        tank1.totalquantity = tank1.totalquantity - int(quantity)
        tank1.save()

        fuelname = request.POST.get('itemName')
        customer = request.POST.get('customer')
        quantity = request.POST.get('quantity')
        platenumber = request.POST.get('platenumber')
        amount = request.POST.get('amount')

        
        rec = record.objects.create(
                username = User.objects.get(username = uname),
                fuelname = fuelname,
                cname = customer,
                quantity = quantity,
                platenumber = platenumber,
                amount = amount
            )
        rec.save()

        # itemId=models.IntegerField(blank=False)
        # fuelname=models.CharField(max_length=255,default="")
        # # fuelname=models.CharField(max_length=255,blank=False)
        # cname=models.CharField(max_length=255)
        # phonenumber=models.IntegerField(blank=False,default="NULL")
        # quantity=models.IntegerField(blank=False)
        # platenumber=models.CharField(max_length=255,default="")
        # amount =models.IntegerField(blank=False)

        return redirect("search")
    return HttpResponse("Error")


def addRecords(request):
    if request.method == "POST":
        fuelname = request.POST.get('itemName')
        customer = request.POST.get('customer')
        quantity = request.POST.get('quantity')
        platenumber = request.POST.get('platenumber')
        amount = request.POST.get('amount')
        phonenumber = request.POST.get('phone')

        uname=request.session["username"]
        ufuelname = request.POST.get('itemName')
        quantity = request.POST.get('quantity')
        
        tank1 = tank.objects.get(fuelname=ufuelname,username=uname)
        tank1.totalquantity = tank1.totalquantity - int(quantity)
        tank1.save()

        uname=request.session["username"]
        rec = record.objects.create(
                username = User.objects.get(username = uname),
                fuelname = fuelname,
                cname = customer,
                quantity = quantity,
                platenumber = platenumber,
                amount = amount,
                phonenumber = phonenumber
            )
        rec.save()
    return redirect('search')

def records(request):
    uname=request.session["username"]
    print(uname)
    records = record.objects.filter(username=uname)
    return render(request,'records.html',{"record":records}) 
    
    # return render(request, "records.html")

def logout_view(request):
    logout(request)
    return redirect('index')



    # if not user:
    #     messages.error(
    #         request,
    #         "Account is invalid",
    #         extra_tags="alert alert-error alert-dismissible show",
    #     )
    #     return redirect("index")
    # else:
    #     return render(request, "login.html")

# def verify(request):
#     a = request.POST.get("uotp")
#     b = request.POST.get("otp")
#     user=request.POST.get("username")
#     # if a == b:
#     #     return redirect("index")
#     return HttpResponse("hello" + str(a) + str(b)+str(user))


# def emailverify(request):
#     subject = "welcome to GFG world"
#     message = f"Hi {user.username}, thank you for registering in geeksforgeeks."
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [
#         user.email,
#     ]
#     send_mail(subject, message, email_from, recipient_list)
