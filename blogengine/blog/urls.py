from django.urls import path
from .views import *

from django.contrib import admin
 

urlpatterns = [
    path('', posts_list, name='posts_list_url'),
	path('category/(<category_slug>/)', Category_view, name='category_detail_url'),
	path('add_to_cart/(<product_slug>)/', add_to_cart_view, name='add_to_cart'),
	path('post/<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
	
	
	
    ] 





