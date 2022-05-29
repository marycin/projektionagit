from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

app_name = 'sklep'
urlpatterns = [
     path('',views.base,name='base'),
    #path('specifics/<int:produkt_id>/',views.detail, name='detail'),
    path('produkt/<int:produkt_id>/',views.produkt_details,name='produkt_details'),

    path('register/',views.register,name='register'),
    path('login_user/',views.login_view,name='login_user'),
    path('logout_user/',views.logout_view,name='logout_user'),
    path('user_site/',views.user_view ,name='user_view'),
    path('orders_site/',views.orders_view,name='orders_view'),
    path('user_modify/',views.user_modify_view,name='user_modify')
]