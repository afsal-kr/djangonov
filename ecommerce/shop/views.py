from django.shortcuts import (render,redirect)
from django.http import HttpResponse
from shop.models import Category,Product
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def allcategories(request):
    c=Category.objects.all()
    return render(request,'category.html',{'c':c})
# Create your views here.

def allproducts(request,p):
    c=Category.objects.get(id=p)
    p=Product.objects.filter(category=c)
    return render(request,'product.html',{'c':c,'p':p})

def detail(request,p):
    p = Product.objects.get(id=p)
    return render(request,'detail.html',{'p':p})

def reg(request):
    if(request.method=="POST"):
        u=request.POST['u']
        p= request.POST['p']
        c = request.POST['c']
        e = request.POST['e']

        if(c==p):
            u=User.objects.create_user(username=u,password=p,email=e,)
            u.save()
            return redirect('shop:allcategories')
        else:
            return HttpResponse("passwords are not same")
    return render(request,'register.html')



def userlogin(request):
    if (request.method=="POST"):
        u = request.POST['u']
        p = request.POST['p']
        user=authenticate(username=u,password=p)
        if user:
            login(request,user)
            return redirect('shop:allcategories')
        else:
            return HttpResponse("invalid")
    return render(request,'login.html')

@login_required
def user_logout(request):
    logout(request)
    return userlogin(request)

def home(request):
    return render(request,'home.html')