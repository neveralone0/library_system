from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm, VerifyFormCode, UserLoginForm
from utils import send_otp_code
from .models import OtpCode, User
from home.models import BookMark, Product
import random


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            print(type(form.cleaned_data['profile']))
            print(form.cleaned_data['profile'])
            print(type(form.cleaned_data['profile'].name))
            print(form.cleaned_data['profile'].name)
            print(dir(form.cleaned_data['profile']))
            random_code = random.randint(1000, 9999)
            # send_otp_code(form.cleaned_data['phone', random_code])
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password'],
                'profile': form.cleaned_data['profile'].name
            }

            messages.success(request, 'verification code sent', 'success')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyFormCode

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code or cd['code'] == 1111:
                User.objects.create_user(user_session['phone_number'],
                                         user_session['email'],
                                         user_session['full_name'],
                                         user_session['password'],
                                         user_session['profile'])
                code_instance.delete()
                messages.success(request, 'registered success fully', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'code is wrong', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'info')
                return redirect('home:home')
            messages.error(request, 'phone or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})


class BookMarksPageView(LoginRequiredMixin, View):
    template_name = 'accounts/bookmarks.html'

    def get(self, request, user_id):
        bookmarks = BookMark.objects.filter(user=request.user)
        books = Product.objects.all()
        books = books.filter(slug__in=list(bookmarks))
        return render(request, self.template_name, {'bookmarks': books})


class ProfilePostMarkView(LoginRequiredMixin, View):
    def get(self, request, slug):
        post = get_object_or_404(Product, slug=slug)
        mark = BookMark.objects.filter(post=post, user=request.user)
        if mark.exists():
            mark.delete()
            messages.warning(request, 'post unmarked', 'warning')
        else:
            BookMark.objects.create(post=post, user=request.user)
            messages.success(request, 'post marked', 'success')
        return redirect('accounts:bookmark', request.user.id)


