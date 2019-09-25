from django.db import models
from django.shortcuts import reverse

from django.utils.text import slugify
from time import time

from django.contrib.auth.models import User
from PIL import Image





class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))

# Create your models here.
class Category(models.Model):
    category_title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)

    def __str__(self):
        return self.category_title

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'category_slug': self.slug})


class ProductManager(models.Manager):
	def all(self, *args, **kwargs):
		return super(ProductManager, self).get_queryset().filter(available=True)


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150,blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='media', help_text='150x150px', default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=True)
    price = models.IntegerField(default=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']

class CartItem(models.Model):
	product = models.ForeignKey(Post, on_delete=models.CASCADE)
	qty = models.PositiveIntegerField(default=1)
	item_total = models.DecimalField(max_digits=900, decimal_places=199, default=0.00)

	def __unicode__(self):
		return "Cart item for product {0}".format(self.product.title)


class Cart(models.Model):
	items = models.ManyToManyField(CartItem, blank=True)
	cart_total = models.DecimalField(max_digits=900, decimal_places=199, default=0.00)

	def __unicode__(self):
		return str(self.id)


