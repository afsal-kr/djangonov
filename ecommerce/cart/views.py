from django.shortcuts import render
from cart.models import Cart,Order,Account
from shop.models import Product
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def cart_view(request):
    u=request.user
    total=0
    cart=Cart.objects.filter(user=u)
    for i in cart:
        total=total+i.quantity*i.product.price
    return render(request,'cart.html',{'cart':cart,'total':total})

@login_required
def addtocart(request,p):
    p=Product.objects.get(id=p)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity+=1
            cart.save()
            p.stock-=1
            p.save()
    except:
        if(p.stock>0):
            cart=Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -= 1
            p.save()

    return cart_view(request)

def cartremove(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        if (cart.quantity > 1):
            cart.quantity -= 1
            cart.save()
            p.stock += 1
            p.save()
        else:
             cart.delete()
             p.stock += 1
             p.save()
    except:
        pass
    return cart_view(request)

def full_remove(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass
    return cart_view(request)

@login_required
def order_form(request):
    if(request.method=="POST"):
        address=request.POST['ad']
        p = request.POST['ph']
        n= request.POST['n']

        u = request.user
        c=Cart.objects.filter(user=u)

        total=0
        for i in c:
            total=total+i.quantity*i.product.price

        try:
            ac=Account.objects.get(acctnum=n)

            if(ac.amount>=total):
                print(ac.amount)

                ac.amount=ac.amount-total
                print(ac.amount)

                ac.save()
                for i in c:
                    o=Order.objects.create(user=u,product=i.product,address=address,phone=p,no_of_item=i.quantity,order_status="paid")
                    o.save()

                c.delete()
                msg="Order Placed Successfully"
                return render(request,'orderdetail.html',{'message':msg})
            else:
                msg="Insufficient Balance"
                return render(request, 'orderdetail.html', {'message': msg})
        except:
            pass

    return render(request,'orderform.html')

def orderview(request):
    u=request.user.id
    cart=Order.objects.filter(user=u)
    return render(request,'orderview.html',{'cart':cart})

# Create your views here.
