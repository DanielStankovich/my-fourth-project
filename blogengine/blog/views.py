from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import Post, Category, CartItem, Cart
from .utils import *
from .forms import  PostForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm


from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from django.contrib import messages
from .forms import  UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.http import HttpResponseRedirect
# Create your views here.

from django.contrib.auth import logout

def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)
    context = {
		'cart': cart
		}
    return render(request, 'blog/cart.html', context)


def logoutUser(request):
    logout(request)      
    return render(request, 'blog/index.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, "blog/users/profile.html", context)



def register(response):
	if response.method == "POST":
		form = RegisterForm(response.POST)
		if form.is_valid():
			form.save()
		return redirect("posts_list_url")
	else:
		form = RegisterForm()
	return render(response, "blog/register/register.html", {"form": form})





def posts_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()
    


    paginator = Paginator(posts, 50)

    

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number())
    else:
        prev_url = ''
    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number())
    else:
        next_url = ''

    categories = Category.objects.all()
    
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart_id
        cart = Cart.objects.get(id=cart_id)

    context = {
		'cart': cart,
		'categories': categories,
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
        }

    return render(request, 'blog/index.html', context=context)


def Category_view(request, category_slug):
	category = Category.objects.get(slug=category_slug)
	products_of_category = Post.objects.filter(category=category)
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	context = {
			'cart': cart,
			'category': category,
			'products_of_category': products_of_category
			}
	return render(request, 'blog/category.html', context)


def add_to_cart_view(request, product_slug):
	product = Post.objects.get(slug=product_slug)
	new_item, _ = CartItem.objects.get_or_create(product=product, item_total=product.price)
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	if new_item not in cart.items.all():
		cart.items.add(new_item)
		cart.save()
		return HttpResponseRedirect('/cart/')
	else:
		return render(request, 'blog/cart.html')


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'











    