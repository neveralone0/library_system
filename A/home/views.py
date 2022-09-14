from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Category, SpecialProduct,Vote
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin
from orders.forms import CartAddForm
from .filters import ProductFilter
from django.contrib.auth.mixins import LoginRequiredMixin


class HomeView(View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Product, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, category_slug=None):
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        filter = ProductFilter(request.GET, queryset=products)
        products = filter.qs
        my_book = SpecialProduct.objects.all()
        special_book = Product.objects.get(pk=my_book[0].spc)

        return render(request, 'home/home.html', {'products': products,
                                                  'categories': categories,
                                                  'filter': filter,
                                                  'special_book': special_book,
                                                  'ins': self.post_instance})


class ProductDetailView(View):
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Product, slug=kwargs['slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()

        can_like = False
        if request.user.is_authenticated and self.post_instance.user_can_like(request.user):
            can_like = True

        return render(request, 'home/detail.html', {'product': product,
                                                    'form': form,
                                                    'can_like': can_like,
                                                    })


class BucketHome(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.all_bucket_objects_task()
        return render(request, self.template_name, {'objects': objects})


class DeleteBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, 'your object will be delete soon.', 'info')
        return redirect('home:bucket')


class DownloadBucketObject(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your download will start soon.', 'info')
        return redirect('home:bucket')


class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, slug):
        post = get_object_or_404(Product, slug=slug)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            like.delete()
            messages.warning(request, 'post disliked', 'warning')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'post liked', 'success')
        return redirect('home:product_detail', post.slug)
