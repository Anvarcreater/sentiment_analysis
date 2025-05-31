from django.urls import path
from . import views

app_name="myshop"
urlpatterns=[
    path("",views.home,name="home"),
    path("home",views.home,name="home"),
    path("viewprodbycat/<int:cat>",views.viewproductbycategory,name="viewprodbycat"),
    path('viewproduct/<int:pk>',views.viewproduct,name="viewproduct"),
    path("signup",views.signup,name="signup"),
    path("login",views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('addtocart',views.addtocart,name="addtocart"),
    path('cart',views.cart,name="cart"),
    path('removecart/<int:pk>',views.removecart,name='removecart'),
    path('order/<int:pk>',views.order,name="order"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('addfeedback/<int:pk>',views.addfeedback,name="addfeedback"),

    
]