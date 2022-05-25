from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

app_name = 'sklep'
urlpatterns = [
    path('',views.base,name='base'),
    path('specifics/<int:produkt_id>/',views.detail, name='detail'),
    path('register/',views.register,name='register'),
    path('login_user/',views.login_view,name='login_user'),
    path('logout_user/',views.logout_view,name='logout_user')
]