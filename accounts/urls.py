from django.urls import path

from accounts import views

urlpatterns = {
    path('user/register', views.UserRegister.as_view()),

    #admin
    path('admin/register', views.AdminRegister.as_view()),

    #check authentication
    path('authenticationcheck', views.AuthenticationCheck.as_view()),
    path('adminauthenticationcheck', views.AdminAuthenticationCheck.as_view()),

    #user list for chat
    path('', views.user_list, name='user_list')

}