from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

app_name = 'sklep'
urlpatterns = [
    path('',views.base,name='base'),
    #path('specifics/<int:produkt_id>/',views.detail, name='detail'),
    
    path('produkt/<int:produkt_id>/',views.produkt_details,name='produkt_details'),
    path('produkt/<int:produkt_id>/add_opinion',views.add_opinion_on_produkt,name='add_opinion_on_produkt'),

    path('user_profile/',views.user_profile_view,name='user_profile'),
    path('update_user_password/',views.update_user_password,name='update_user_password'),


    path('register/',views.register,name='register'),
    path('login_user/',views.login_view,name='login_user'),
    path('logout_user/',views.logout_view,name='logout_user'),

    path('user_site/',views.user_view ,name='user_view'),
    path('orders_site/',views.orders_view,name='orders_view'),
    path('add_adres/',views.add_adres,name='add_adres'),
    path('adres/<int:adres_id>/',views.egz_adres_modify_view,name="adres_mod")
]