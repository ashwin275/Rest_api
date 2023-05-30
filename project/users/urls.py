
from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.Logoutview.as_view(),name='logout'),

# user
    path('userview/',views.UserView.as_view(),name='userview'),
    path('userprofile/<int:pk>/',views.UserView.as_view(),name='userprofile'),

#    admin
    path('userList/',views.adminView.as_view(),name='userList'),
    path('useredit/<int:pk>/',views.adminView.as_view(),name='useredit')
   
]