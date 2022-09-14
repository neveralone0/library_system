from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from accounts.models import User


class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='scategory', null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:category_filter', args=[self.slug,])


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name='products')
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    pages = models.PositiveIntegerField(default=100, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField() # upload_to='products/%Y/%m/%d/'
    description = RichTextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:product_detail', args=[self.slug, ])

    def likes_count(self):
        return self.pvotes.count()

    def user_can_like(self, user):
        user_like = user.uvotes.filter(post=self)
        try:
            if user_like.exists():
                return True
            return False
        except:
            pass

class SpecialProduct(models.Model):
    # spc = models.OneToOneField(Product, on_delete=models.DO_NOTHING)
    spc = models.IntegerField()


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes')
    post = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pvotes')

    def __str__(self):
        return f'{self.user} liked {self.post.slug}'

