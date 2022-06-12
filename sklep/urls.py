from django.urls import path, include

from . import views
from django.contrib.auth import views as auth_views

app_name = 'sklep'
urlpatterns = [
    path('',views.base,name='base'),
    #path('specifics/<int:produkt_id>/',views.detail, name='detail'),
    
    path('produkt/<int:produkt_id>/',views.produkt_details,name='produkt_details'),
    path('produkt/<int:produkt_id>/add_opinion',views.add_opinion_on_produkt,name='add_opinion_on_produkt'),
    path('produkt/<int:produkt_id>/add_to_cart',views.add_to_cart,name='add_to_cart'),

    path('user_profile/',views.user_profile_view,name='user_profile'),
    path('update_user_password/',views.update_user_password,name='update_user_password'),

    path('register/',views.register,name='register'),
    path('login_user/',views.login_view,name='login_user'),
    path('logout_user/',views.logout_view,name='logout_user'),

    path('shopping_cart/',views.shopping_cart,name='shopping_cart'),
    path('delete_from_cart/',views.delete_from_cart,name='delete_from_cart'),
    path('address_selection/',views.address_selection,name='address_selection'),
    path('checkout/',views.checkout,name='checkout'),
    path('order_summary',views.order_summary,name='order_summary'),
    path('decrease_amout_of_produkt',views.decrease_amount_of_produkt,name='decrease_amount'),
    path('increase_amout_of_produkt',views.increase_amount_of_produkt,name='increase_amount'),

    path('searchProduct/', views.searchBar, name='searchProduct'),

    path('user_site/',views.user_view ,name='user_view'),
    path('orders_site/',views.orders_view,name='orders_view'),
    path('add_adres/',views.add_adres,name='add_adres'),
    path('adres/<int:adres_id>/',views.egz_adres_modify_view,name="adres_mod"),
    path('adres_del/<int:adres_id>/',views.del_adres,name="del_adres"),
    path('user_mod/',views.user_dat_mod,name='user_dat_mod'),
    path('zamowienie_szcz/<int:id_zamowienia>/',views.zamowienie_szcz,name='order_detail'),

]