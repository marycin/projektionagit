from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

app_name = 'sklep'
urlpatterns = [
    path('',views.base,name='base'), 
    #path('specifics/<int:produkt_id>/',views.detail, name='detail'),
    
    path('produkt/<int:produkt_id>/',views.produkt_details,name='produkt_details'), #Marcin
    path('produkt/<int:produkt_id>/add_opinion',views.add_opinion_on_produkt,name='add_opinion_on_produkt'), #Karolina
    path('produkt/<int:produkt_id>/add_to_cart',views.add_to_cart,name='add_to_cart'), #Marcin

    path('user_profile/',views.user_profile_view,name='user_profile'), #zmiana hasla Sroczyk
    path('update_user_password/',views.update_user_password,name='update_user_password'), #Sroczyk

    path('register/',views.register,name='register'), #Basznianin
    path('login_user/',views.login_view,name='login_user'), #Marcin
    path('logout_user/',views.logout_view,name='logout_user'), #Marcin

    path('shopping_cart/',views.shopping_cart,name='shopping_cart'), #Basznianin
    path('delete_from_cart/',views.delete_from_cart,name='delete_from_cart'), #Basznianin
    path('address_selection/',views.address_selection,name='address_selection'), #Kateryna
    path('checkout/',views.checkout,name='checkout'), #Kateryna
    path('order_summary',views.order_summary,name='order_summary'), #Kateryna


    #path('decrease_amout_of_produkt',views.decrease_amount_of_produkt,name='decrease_amount'),
    #path('increase_amout_of_produkt',views.increase_amount_of_produkt,name='increase_amount'),

    path('searchProduct/', views.searchBar, name='searchProduct'), #Karolina

    path('user_site/',views.user_view ,name='user_view'), #Maciek
    path('orders_site/',views.orders_view,name='orders_view'), #Grzesiu
    path('add_adres/',views.add_adres,name='add_adres'), #Maciek
    path('adres/<int:adres_id>/',views.egz_adres_modify_view,name="adres_mod"), #Maciek
    path('adres_del/<int:adres_id>/',views.del_adres,name="del_adres"), #Maciek
    path('user_mod/',views.user_dat_mod,name='user_dat_mod'), #Grzesiu
    path('zamowienie_szcz/<int:id_zamowienia>/',views.zamowienie_szcz,name='order_detail'), #Grzesiu


    path('filtr/<str:filter>/',views.filter_view,name='filter_view'),
]