from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import Product,Category,Cart,Orderlist,Feedback
from .forms import SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
import json 
import numpy 
import tensorflow as tf
from transformers import BertTokenizer,TFBertForSequenceClassification

# Create your views here.

# loading the trained model
model=TFBertForSequenceClassification.from_pretrained('./myapp/saved_bert_model2')
tokenizer=BertTokenizer.from_pretrained('./myapp/saved_bert_model2')

def home(request):
    products=Product.objects.all()
    category=Category.objects.all()
    return render(request,'home.html',{"products":products,"category":category})

def viewproductbycategory(request,cat):
    products=Product.objects.filter(category=cat)
    category=Category.objects.get(pk=cat)
    return render(request,"viewprodbycat.html",{"products":products,"category":category})

def viewproduct(request,pk):
    try:
        product=Product.objects.get(pk=pk)
        related=Product.objects.filter(category=product.category).exclude(pk=product.id)
        feedbacks=Feedback.objects.filter(product=pk)
        positive=0
        negative=0
        neutral=0
        for i in feedbacks:
            if i.status=='positive':
                positive+=1
            elif i.status =="negative":
                negative+=1
            else:
                neutral+=1
        return render(request,"viewproduct.html",{"product":[product],"related":related,"feedbacks":feedbacks,"positive":positive,"negative":negative,"neutral":neutral})
    except Exception as e:
        return HttpResponse(f"Error is :{e}")

def signup(request):
        form =SignupForm()
        if request.method == "POST":
            form=SignupForm(request.POST)
            if form.is_valid():
                user=form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request,"success you can login")
                return redirect("/login")
            else:
                return render(request,"signup.html",{"form":form})
        return render(request,"signup.html")

def login(request):
    form=LoginForm()
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                auth_login(request,user)
                print("login success")
                return redirect("myshop:dashboard")
    return render(request,"login.html",{"form":form})


def logout(request):
    auth_logout(request)
    return redirect('myshop:home')


def addtocart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.is_authenticated:
            data=json.load(request)
            product_qty=data['product_qty']
            product_id=data['pid']
            print(product_qty)
            print(type(product_qty))
            user_id=request.user.id
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=user_id,products=product_id):
                    return JsonResponse({'status':'product is already exist in the cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,products=product_status,product_quantity=product_qty)
                        return JsonResponse({"status":'product added to cart successfully'},status=200)
                    else:
                        return JsonResponse({'product stock not available'},status=200) 
        else:
            return JsonResponse({'status':'login to add to cart'},status=200)
    else:
        return JsonResponse({'status':'invalid Access'},status=200) 

def cart(request):
    if request.user.is_authenticated:
        cartproducts=Cart.objects.filter(user=request.user)
        total=0
        for i in cartproducts:
            total+=i.products.price*i.product_quantity
        return render(request,"cart.html",{"cartprod":cartproducts,"total":total})
    else:
        return redirect('myshop:home')

def removecart(request,pk):
    Cart.objects.get(pk=pk).delete()
    return redirect('myshop:cart')

def order(request,pk):
    cartdata=Cart.objects.filter(pk=pk)
    amount=0
    user=None
    products=None
    for i in cartdata:
        amount+=i.products.price*i.product_quantity
        user=i.user
        products=i.products
    if request.method=="POST":
        username=request.POST.get('username')
        phone=request.POST.get('phone')
        address=request.POST.get('address')
        print({'username':username,"phone":phone,"address":address,'amount':amount,'user':user,'products':products})
        Orderlist.objects.create(user=user,product=products,username=username,phone=phone,address=address,amount=amount,status="ordered")
        return redirect('myshop:dashboard')
    return render(request,"order.html")

def dashboard(request):
    orderdata=Orderlist.objects.filter(user=request.user)
    return render(request,"dashboard.html",{"orderdata":orderdata})

def sentiment(feedback):
    new=[feedback]
    inputs=tokenizer(new,truncation=True,padding=True,return_tensors="tf")
    output=model.predict(dict(inputs)).logits
    predicted_model=tf.argmax(output,axis=1).numpy()[0]
    return predicted_model

def addfeedback(request,pk):
    if request.method =="POST":
        feedback=request.POST.get('feedback')
        sent=sentiment(feedback)
        status=None
        if sent == 1:
            status="positive"
        elif sent == 2:
            status="neutral"
        else:
            status="negative"
        orderdata=Orderlist.objects.filter(pk=pk)
        product=None
        for i in orderdata:
            product=i.product
        Feedback.objects.create(user=request.user,product=product,feedback=feedback,status=status)
        print(feedback,status,request.user,product)
        return redirect('myshop:dashboard')