from django.contrib import admin
from . import models

from .models import Category
from .models import Post
# Register your models here.
from .models import Profile
from .models import CartItem
from .models import Cart

admin.site.register(CartItem)

admin.site.register(Cart)

admin.site.register(Profile)


admin.site.register(models.Post)

admin.site.register(models.Category)

