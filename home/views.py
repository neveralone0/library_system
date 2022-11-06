from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Product, Category, SpecialProduct, Comment, Vote, BookMark
from .forms import CommentCreateForm, CommentReplyForm
from . import tasks
from utils import IsAdminUserMixin
from orders.forms import CartAddForm
from .filters import ProductFilter
from better_profanity import profanity


class HomeView(View):
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
        special_like = special_book.user_can_like(request.user)
        can_like = list()
        if request.user.is_authenticated:
            for count in range(len(products)):
                if products[count].user_can_like(request.user):
                    can_like.append('\u2764')
                else:
                    can_like.append('💔')
        products = list(products)
        products = zip(products, can_like)
        return render(request, 'home/home.html', {'products': products,
                                                  'categories': categories,
                                                  'filter': filter,
                                                  'special_book': special_book,
                                                  'special_like': special_like,
                                                  })


class ProductDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()

        can_like = False
        if request.user.is_authenticated and product.user_can_like(request.user):
            can_like = True
        comments = product.pcomments.filter(is_reply=False)
        return render(request, 'home/detail.html', {
            'can_like': can_like,
            'product': product,
            'comments': comments,
            'form': form,
            'form': self.form_class,
            'reply_form': self.form_class_reply,
        })

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # check for badwords
            check = profanity.contains_profanity(form.cleaned_data['body'])
            if check:
                messages.error(request, 'shame on you!', 'danger')
                return redirect('home:home')
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'comment submitted', 'success')
            return redirect('home:product_detail', self.post_instance.slug)


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


class PostAddCommentView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Product, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)

        if form.is_valid():
            # check for badwords
            check = profanity.contains_profanity(form.cleaned_data['body'])
            if check:
                messages.error(request, 'shame on you!', 'danger')
                return redirect('home:home')
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, 'your reply submitted', 'success')
        return redirect('home:product_detail', post.slug)


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


class HomePostLikeView(LoginRequiredMixin, View):
    def get(self, request, slug):
        post = get_object_or_404(Product, slug=slug)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            like.delete()
            messages.warning(request, 'post disliked', 'warning')
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'post liked', 'success')
        return redirect('home:home')


class HomePostMarkView(LoginRequiredMixin, View):
    def get(self, request, slug):
        post = get_object_or_404(Product, slug=slug)
        mark = BookMark.objects.filter(post=post, user=request.user)
        if mark.exists():
            mark.delete()
            messages.warning(request, 'post unmarked', 'warning')
        else:
            BookMark.objects.create(post=post, user=request.user)
            messages.success(request, 'post marked', 'success')
        return redirect('home:home')

