
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('userview/',views.UserView.as_view(),name='userview'),
    path('logout/',views.Logoutview.as_view(),name='logout'),
    path('userList/',views.UserListview.as_view(),name='userList')
   
]