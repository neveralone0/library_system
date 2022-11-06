from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('book-api/', views.BookAPI.as_view(), name='book_api'),
    path('user-register-api/', views.UserRegistrationAPI.as_view(), name='user_register_api'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('bookmarks/<int:user_id>', views.BookMarksPageView.as_view(), name='bookmark'),
    path('bookmarks-change/<slug:slug>', views.ProfilePostMarkView.as_view(), name='profile_bookmark'),
]
