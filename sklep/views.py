from email import message
from lib2to3.pgen2.token import OP
from mimetypes import common_types
from multiprocessing import context
from django.http import Http404
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime
from decimal import Decimal
import re

from .forms import  ExtendedUserCreationForm,klientForm
from .models import Adres, Platnosci, PozycjaZamowienia, Produkt, Opinie,Klient, Produkt_Rozmiar, RodzajePlatnosci, Zamowienie, RodzajWysylki,KartyPlatnicze
# Create your views here.

def base(request):
    produkt_list = Produkt.objects.all().order_by('-id')[:10]
    context = {'produkt_list' : produkt_list}
    return render(request, 'sklep/base/base.html',context)

def detail(request, produkt_id):
    try:
        produkt = Produkt.objects.get(pk = produkt_id)
    except Produkt.DoesNotExist:
        raise Http404('Produkt nie istnieje, łooot?')
    return render(request, 'sklep/detail.html',{
        'produkt' : produkt
    })

def produkt_details(request,produkt_id):
    try:
        produkt = Produkt.objects.get(pk=produkt_id)
        rozmiar = Produkt_Rozmiar.objects.filter(produkt = produkt)
        opinie = Opinie.objects.all()
    except:
        raise Http404('Produkt nie istnieje, łooot?')
    return render(request, 'sklep/base/produkt-details.html',{
        'produkt' : produkt,
        'rozmiar' : rozmiar,
        'opinie' : opinie
    })

def add_opinion_on_produkt(request, produkt_id):
    print('Dodano opinie o produkcie',produkt_id)
    produkt = Produkt.objects.get(pk=produkt_id)
    opinie = Opinie.objects.all()
    if request.method =='POST':
        komentarz = request.POST['komentarz']
        ocena = request.POST['ocena']
        klient = Klient.objects.get(user = request.user)

        opinia = Opinie(komentarz = komentarz, ocena = ocena, produkt = produkt, klient = klient)
        opinia.save()
        return redirect('sklep:produkt_details', produkt_id)
    # return render(request,'sklep/base/base__produkt-details.html',{ 
    #     'produkt' : produkt,
    #     'opinie' : opinie
    # })                        ## chyba niepotrzebne, ale kto wie


def register(request):
    if request.method =='POST':
        form = ExtendedUserCreationForm(request.POST)
        klient_form = klientForm(request.POST)
        if form.is_valid() and klient_form.is_valid():
            print("Utworzono konto")
            user = form.save() 
            klient = klient_form.save(commit=False)
            klient.user = user
            klient.save()
            return redirect('sklep:base')
    else:
        form = ExtendedUserCreationForm(request.POST)
        klient_form = klientForm(request.POST)
    context = {
        'form' : form,
        'klient_form' : klient_form
    }
    return render(request, 'sklep/user/register.html', context)

def user_profile_view(request):
    return render(request,'sklep/user/user_profile.html')

def update_user_password(request):
    if request.method == 'POST':
        usr = User.objects.get(username = request.user.username)
        new_password = request.POST['new_password']
        usr.set_password(new_password)
        usr.save()
        return redirect('sklep:base')

def login_view(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            print('Zalogowano')
            return redirect('sklep:base')
        else:
            print('Nie udało się zalogować :c')
            return redirect('sklep:login_user')
    
    return render(request, 'sklep/user/login_user.html', {})


def logout_view(request):
    logout(request)
    return redirect('sklep:base')

def shopping_cart(request):
    context = {}
    if request.user.is_authenticated:
        aktualny_klient = Klient.objects.get(user=request.user)
        aktualne_zamowienie = Zamowienie.objects.filter(
            klient = aktualny_klient,
            czy_zamowione=False)
        
        czy_puste=False
        if len(aktualne_zamowienie) ==0:
            czy_puste=True
            return render(request,'sklep/order/shopping_cart.html',{
                'czy_puste' : czy_puste
            })
 
        context = {
            'aktualne_zamowienie' : aktualne_zamowienie[0],
            'czy_puste' : czy_puste
            }
    return render(request,'sklep/order/shopping_cart.html',context)



def add_to_cart(request, produkt_id):
    klient = get_object_or_404(Klient, user=request.user)
    produkt = Produkt.objects.get(id=produkt_id)
    wybrany_rozmiar = request.POST['produkt-size']
    klient_zamowienie, status = Zamowienie.objects.get_or_create(
        klient = klient,
        data_zamowienia = datetime.now(),
        czy_zamowione = False)

    pozycja_zamowienia = PozycjaZamowienia.objects.create(
        ilosc = 1,
        produkt = produkt,
        rozmiar = wybrany_rozmiar)

    for p_z in klient_zamowienie.get_pozycje_zamowienia():
        print(p_z.produkt.pk, p_z.rozmiar)
        print(pozycja_zamowienia.produkt.pk, pozycja_zamowienia.rozmiar)
        if (int(p_z.produkt.pk) == int(pozycja_zamowienia.produkt.pk) and int(p_z.rozmiar) == int(pozycja_zamowienia.rozmiar)):
            pozycja_zamowienia.delete()
            p_z.ilosc +=1
            p_z.save()
            klient_zamowienie.save()
            return redirect('sklep:shopping_cart')
    
    klient_zamowienie.pozycje_zamowienia.add(pozycja_zamowienia)
    klient_zamowienie.save()
    return redirect('sklep:shopping_cart')

def delete_from_cart(request):
    klient = get_object_or_404(Klient, user=request.user)
    PozycjaZamowienia.objects.get(pk  = request.POST['to_delete']).delete()
    zamowienie = Zamowienie.objects.get(klient = klient, czy_zamowione = False)
    if len(zamowienie.get_pozycje_zamowienia()) ==0:
        zamowienie.delete()
    messages.info(request,"Usunięto produkt z koszyka")
    return redirect('sklep:shopping_cart')

def address_selection(request):
    aktualny_klient = get_object_or_404(Klient, user=request.user)
    lista_adresow = Adres.objects.filter(klient = aktualny_klient)
    zamowienie= Zamowienie.objects.get(klient = aktualny_klient,czy_zamowione = False)
    rodzaje_wysylek = RodzajWysylki.objects.all()
    context = {
        'klient' : aktualny_klient,
        'lista_adresow' : lista_adresow,
        'aktualne_zamowienie' : zamowienie,
        'rodzaje_wysylek' : rodzaje_wysylek
    }
    return render(request,'sklep/order/address_selection.html', context)

def checkout(request):
    if request.method=='POST':
        aktualny_klient = get_object_or_404(Klient, user=request.user)
        platnosci = RodzajePlatnosci.objects.all()
        adres = Adres.objects.get(pk = request.POST['adres'])
        rodzaj_wysylki = RodzajWysylki.objects.get(pk = request.POST['wysylka'])
        
        zamowienie= Zamowienie.objects.get(
            klient = aktualny_klient,
            czy_zamowione = False)
            
        zamowienie.adres = adres
        zamowienie.rodzaj_wysylki = rodzaj_wysylki
        zamowienie.save()



        karty_platnicze_klienta = KartyPlatnicze.objects.filter(klient = aktualny_klient)
        print(zamowienie.adres.miejscowosc)
        context = {
            'klient' : aktualny_klient,
            'aktualne_zamowienie' : zamowienie,
            'rodzaje_platnosci' : platnosci,
            'karty_platnicze' : karty_platnicze_klienta
        }
    return render(request, 'sklep/order/checkout.html',context)

def order_summary(request):
    rodzaj_platnosci = RodzajePlatnosci.objects.get(pk = request.POST['rodzaj_platnosci'])
    aktualny_klient = get_object_or_404(Klient, user=request.user)

    zamowienie= Zamowienie.objects.get(klient = aktualny_klient,czy_zamowione = False)
    t_kwota = zamowienie.get_kwota_zamowienia()
    platnosc = Platnosci.objects.get_or_create(
        zamowienie = zamowienie, 
        kwota = t_kwota,
        rodzaj_platnosci = rodzaj_platnosci,
        data_zaksiegowania = datetime.now())
    zamowienie.czy_zamowione = True
    zamowienie.czy_oplacono = True
    zamowienie.save()

    context = {
        'zamowienie' : zamowienie,
        'platnosc' : platnosc
    }
        
    return render(request, 'sklep/order/summary.html', context)

def increase_amount_of_produkt(request):
    pozycja = PozycjaZamowienia.objects.get(pk  = request.POST['to_change'])
    if pozycja.ilosc < pozycja.produkt.ilosc_dostepnego:
        pozycja.ilosc = pozycja.ilosc + 1
        pozycja.save()
    return redirect('sklep:shopping_cart')

def decrease_amount_of_produkt(request):
    pozycja = PozycjaZamowienia.objects.get(pk  = request.POST['to_change'])
    if pozycja.ilosc > 1:
        pozycja.ilosc = pozycja.ilosc - 1
        pozycja.save()
    return redirect('sklep:shopping_cart')


def searchBar(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        dopasowanie = re.search(' ', query)
        if dopasowanie:
            temp = query.split()
            query1 = temp[0];
            query2 = temp[1];
            if query:
                produkt_list = Produkt.objects.filter(marka__icontains=query1) or Produkt.objects.filter(model__icontains=query1) or Produkt.objects.filter(marka__icontains=query2) or Produkt.objects.filter(model__icontains=query2)
                return render(request, 'sklep/base/searchProduct.html', {'produkt_list':produkt_list})
            else:
                print("Brak produktu")
                return render(request, 'sklep/base/searchProduct.html', {})
        else:

            if query:
                produkt_list = Produkt.objects.filter(marka__icontains=query) or Produkt.objects.filter(model__icontains=query)
                return render(request, 'sklep/base/searchProduct.html', {'produkt_list':produkt_list})
            else:
                print("Brak produktu")
                return render(request, 'sklep/base/searchProduct.html', {})

def egz_adres_modify_view(request,adres_id):
    adres=Adres.objects.get(id=adres_id)
    if request.method=='POST':
        adres_form=AdresForm(request.POST)
        if adres_form.is_valid():
            print("modyfikowanie adresu")
            adres.miejscowosc=adres_form.cleaned_data['miejscowosc']
            adres.ulica=adres_form.cleaned_data['ulica']
            adres.kod_pocztowy=adres_form.cleaned_data['kod_pocztowy']
            adres.numer_domu=adres_form.cleaned_data['numer_domu']
            adres.numer_lokalu=adres_form.cleaned_data['numer_lokalu']
            adres.save()
            return redirect('sklep:user_view')
    else:
        if request.user.is_authenticated:
            adres_form=AdresForm(initial={
                'miejscowosc':adres.miejscowosc,
                'ulica':adres.ulica,
                'kod_pocztowy':adres.kod_pocztowy,
                'numer_domu':adres.numer_domu,
                'numer_lokalu':adres.numer_lokalu,
            })
        else:
            return redirect('sklep:base')

    return render(request,'sklep/user/user_egz_adres.html',{
        'adres_form':adres_form,
        'adres_id':adres.id,
    })

def del_adres(request,adres_id):
    adres=Adres.objects.get(id=adres_id)
    if request.method=='POST':
        adres.delete()
    return redirect('sklep:user_view')

def user_dat_mod(request):
    if request.user.is_authenticated:
        klient=Klient.objects.get(user=request.user)
        if request.method=='POST':
            user_form=UserDataModification(request.POST)
            klient_form=klientForm(request.POST)
            if user_form.is_valid():
                print('zmieniam dane')
                klient.user.username=user_form.cleaned_data['username']
                klient.user.email=user_form.cleaned_data['email']
                klient.user.first_name=user_form.cleaned_data['first_name']
                klient.user.last_name=user_form.cleaned_data['last_name']
                klient.user.save()
            if klient_form.is_valid():
                klient.telefon=klient_form.cleaned_data['telefon']
                klient.data_urodzenia=klient_form.cleaned_data['data_urodzenia']
                klient.save()
            return redirect('sklep:user_view')
        else:
            user_form=UserDataModification(initial={
                'username':klient.user.username,
                'email':klient.user.email,
                'first_name':klient.user.first_name,
                'last_name':klient.user.last_name,
            })
            klient_form=klientForm(initial={
                'telefon':klient.telefon,
                'data_urodzenia':klient.data_urodzenia
            })
        return render(request,'sklep/user/user_dat_mod.html',{
        'user_mod_form':user_form,
        'klient_mod_form':klient_form
    })
    else:
        return redirect('sklep:base')

def zamowienie_szcz(request,id_zamowienia):
    if request.user.is_authenticated:
        zamowienie=Zamowienie.objects.get(id=id_zamowienia)
        Pozycja_Zamowienia=zamowienie.pozycje_zamowienia.all()
        kwota_zamowienia=zamowienie.get_kwota_zamowienia()
        
        return render(request,'sklep/user/order_detail.html',{
            'zamowienie':zamowienie,
            'pozycja_zamowienia':Pozycja_Zamowienia,
            'kwota':kwota_zamowienia,
        })
    else:
        return redirect('sklep:base')
    

