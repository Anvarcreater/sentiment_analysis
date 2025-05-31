from django.contrib import admin
from .models import Category,Product,Cart,Orderlist,Feedback
# Register your models here.



admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Orderlist)
admin.site.register(Feedback)