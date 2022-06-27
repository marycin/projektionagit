from ast import Str
from email import message
import email
from lib2to3.pgen2.token import OP
from mimetypes import common_types
from multiprocessing import context
from django.http import Http404
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from datetime import datetime
from decimal import Decimal
import re
from django.contrib.sessions.backends.db import SessionStore
from django.core.mail import mail_admins
from numpy import full
from django.core.mail import send_mail

from .forms import  ExtendedUserCreationForm,klientForm,UserDataModification,AdresForm,UserNickMod,KartyPlatniczeForm
from .models import Adres, Kategoria, Platnosci, PozycjaZamowienia, Produkt, Opinie,Klient, Produkt_Rozmiar, RodzajePlatnosci, Zamowienie, RodzajWysylki,KartyPlatnicze, Zdjecia
from .models import Adres, Platnosci, Podkategoria, PozycjaZamowienia, Produkt, Opinie,Klient, Produkt_Rozmiar, RodzajePlatnosci, Zamowienie, RodzajWysylki,KartyPlatnicze
# Create your views here.

def initialize(request):
    request.session['nav_cat']=[]
    kategorie=Kategoria.objects.all()
    for k in kategorie:
        print(k.nazwa)
        request.session['nav_cat'].append(k.nazwa)


def base(request): #
    initialize(request)
    produkt_list = Produkt.objects.all().order_by('-id')[:10]
    context = {'produkt_list' : produkt_list}
    return render(request, 'sklep/base/base.html',context)

def detail(request, produkt_id):
    initialize(request)
    try:
        produkt = Produkt.objects.get(pk = produkt_id)
    except Produkt.DoesNotExist:
        raise Http404('Produkt nie istnieje, łooot?')
    return render(request, 'sklep/detail.html',{
        'produkt' : produkt
    })

def produkt_details(request,produkt_id):
    initialize(request)
    try:
        produkt = Produkt.objects.get(pk=produkt_id)
        rozmiar = Produkt_Rozmiar.objects.filter(produkt = produkt)
        opinie = Opinie.objects.all()
        zdjecia=Zdjecia.objects.filter(produkt=produkt)
        print(len(zdjecia))
    except:
        raise Http404('Produkt nie istnieje, łooot?')
    return render(request, 'sklep/base/produkt-details.html',{
        'produkt' : produkt,
        'rozmiar' : rozmiar,
        'opinie' : opinie,
        'zdjecia':zdjecia
    })

def add_opinion_on_produkt(request, produkt_id):
    initialize(request)
    print('Dodano opinie o produkcie',produkt_id)
    produkt = Produkt.objects.get(pk=produkt_id)
    opinie = Opinie.objects.all()
    if request.method =='POST':
        try:
            komentarz = request.POST['komentarz']
            ocena = request.POST['ocena']
            klient = Klient.objects.get(user = request.user)
        except:
            return redirect('sklep:produkt_details', produkt_id)

        opinia = Opinie(komentarz = komentarz, ocena = ocena, produkt = produkt, klient = klient)
        opinia.save()
        return redirect('sklep:produkt_details', produkt_id)
    # return render(request,'sklep/base/base__produkt-details.html',{ 
    #     'produkt' : produkt,
    #     'opinie' : opinie
    # })                        ## chyba niepotrzebne, ale kto wie


def register(request):
    initialize(request)
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
    initialize(request)
    return render(request,'sklep/user/user_profile.html')

def update_user_password(request):
    initialize(request)
    if request.method == 'POST':
        usr = User.objects.get(username = request.user.username)
        new_password = request.POST['new_password']
        usr.set_password(new_password)
        usr.save()
        return redirect('sklep:base')

def login_view(request):
    initialize(request)
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
    initialize(request)
    logout(request)
    return redirect('sklep:base')

def shopping_cart(request):
    initialize(request)
    context = {}
    if request.user.is_authenticated:
        aktualny_klient = Klient.objects.get(user=request.user)
        aktualne_zamowienie = Zamowienie.objects.filter(
            klient = aktualny_klient,
            czy_zamowione=False)
        
        czy_puste=False
        #print(aktualne_zamowienie[0].czy_puste())
        if len(aktualne_zamowienie) ==0:
            czy_puste=True
            return render(request,'sklep/order/shopping_cart.html',{
                'czy_puste' : czy_puste
            })
        zamowienie_do_zwrotu = aktualne_zamowienie[0]
        context = {
            'aktualne_zamowienie' : zamowienie_do_zwrotu,
            'czy_puste' : czy_puste
            }
    return render(request,'sklep/order/shopping_cart.html',context)



def add_to_cart(request, produkt_id):
    initialize(request)
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
        rozmiar = wybrany_rozmiar,
        data_dodania = datetime.now())

    for p_z in klient_zamowienie.get_pozycje_zamowienia():
        initialize(request)
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
    initialize(request)
    klient = get_object_or_404(Klient, user=request.user)
    PozycjaZamowienia.objects.get(pk  = request.POST['to_delete']).delete()
    zamowienie = Zamowienie.objects.get(klient = klient, czy_zamowione = False)
    if len(zamowienie.get_pozycje_zamowienia()) ==0:
        zamowienie.delete()
        print(zamowienie)
    messages.info(request,"Usunięto produkt z koszyka")
    return redirect('sklep:shopping_cart')

def address_selection(request):
    initialize(request)
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
    initialize(request)
    if request.method=='POST':
        aktualny_klient = get_object_or_404(Klient, user=request.user)
        platnosci = RodzajePlatnosci.objects.all()
        
        rodzaj_wysylki = RodzajWysylki.objects.get(pk = request.POST['wysylka'])
        
        zamowienie= Zamowienie.objects.get(
            klient = aktualny_klient,
            czy_zamowione = False)
        full_kwota = zamowienie.get_kwota_zamowienia() + rodzaj_wysylki.cena
        if request.POST['adres'] == 'new-adress':
            if request.POST['numer_lokalu']:
                adres = Adres.objects.create(
                miejscowosc = request.POST['miejscowosc'],
                ulica = request.POST['ulica'],
                numer_domu = request.POST['numer_domu'],
                numer_lokalu = request.POST['numer_lokalu'],
                kod_pocztowy = request.POST['kod_pocztowy']
            )
            else:
                adres = Adres.objects.create(
                miejscowosc = request.POST['miejscowosc'],
                ulica = request.POST['ulica'],
                numer_domu = request.POST['numer_domu'],
                kod_pocztowy = request.POST['kod_pocztowy']
            )

        else:
            adres = Adres.objects.get(pk = request.POST['adres'])  
        zamowienie.adres = adres
        zamowienie.rodzaj_wysylki = rodzaj_wysylki
        zamowienie.save()



        karty_platnicze_klienta = KartyPlatnicze.objects.filter(klient = aktualny_klient)
        context = {
            'klient' : aktualny_klient,
            'aktualne_zamowienie' : zamowienie,
            'rodzaje_platnosci' : platnosci,
            'karty_platnicze' : karty_platnicze_klienta,
            'full_kwota' : full_kwota

        }
    return render(request, 'sklep/order/checkout.html',context)

def order_summary(request):
    initialize(request)
    rodzaj_platnosci = RodzajePlatnosci.objects.get(pk = request.POST['rodzaj_platnosci'])
    aktualny_klient = get_object_or_404(Klient, user=request.user)

    zamowienie= Zamowienie.objects.get(klient = aktualny_klient,czy_zamowione = False)
    full_kwota = zamowienie.get_kwota_zamowienia() + zamowienie.rodzaj_wysylki.cena
    platnosc = Platnosci.objects.get_or_create(
        zamowienie = zamowienie,
        data_zaksiegowania = datetime.now(),
        rodzaj_platnosci = rodzaj_platnosci,
        kwota = full_kwota
        )
    zamowienie.czy_zamowione = True
    zamowienie.czy_oplacono = True
    zamowienie.save()

    full_kwota = zamowienie.get_kwota_zamowienia() + zamowienie.rodzaj_wysylki.cena
    nazwa_platnosci = rodzaj_platnosci.nazwa


    context = {
        'zamowienie' : zamowienie,
        'platnosc' : platnosc,
        'full_kwota' : full_kwota,
        'nazwa_platnosci' : nazwa_platnosci
    }
    return render(request, 'sklep/order/summary.html', context)
            
    

def updateItem(request):
    initialize(request)
    data = json.loads(request.body)
    print(data['pzId'])
    pz_id = data['pzId']
    action = data['action']
    p_z = PozycjaZamowienia.objects.get(id = pz_id)
    if action=='increase':
        p_z.ilosc = (p_z.ilosc + 1)
    elif action == 'decrease' and p_z.ilosc>1:
        p_z.ilosc = (p_z.ilosc - 1)

    p_z.save()

    return JsonResponse('Item increased',safe = False)

def updateShippingItem(request):
    initialize(request)
    data = json.loads(request.body)
    wysylka_id = data['wysylkaId']
    print(wysylka_id)

    klient = Klient.objects.get(user = request.user)

    zamowienie = Zamowienie.objects.get(klient = klient, czy_zamowione = False)
    wysylka = RodzajWysylki.objects.get(pk = wysylka_id)
    zamowienie.rodzaj_wysylki = wysylka
    zamowienie.save()

    return JsonResponse('Item increased',safe = False)



def searchBar(request):
    initialize(request)
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

def orders_view(request):
    initialize(request)

    if request.user.is_authenticated:
        curr_klient=Klient.objects.get(user=request.user.id)
        zamowienia=Zamowienie.objects.filter(klient=curr_klient, czy_zamowione = True)
        ilosc=len(zamowienia)
        #return HttpResponse(request.user.id)
        return render(request, 'sklep/user/orders_view.html',{
            'zamowienia':zamowienia,
            'ilosc':ilosc
        })
    else:
        return redirect('sklep:base')
        #return render(request, 'sklep/user_view.html')

def user_view(request):
    initialize(request)
    if request.user.is_authenticated:
        try: 
            uzytkownik=Klient.objects.get(user=request.user.id)
        except:
            return Http404
        adresy=Adres.objects.filter(klient = uzytkownik)
        kartyplatnicze=KartyPlatnicze.objects.filter(klient=uzytkownik)
        return render(request,'sklep/user/user_view.html',{
            'data_ur':uzytkownik.data_urodzenia,
            'telefon':uzytkownik.telefon,
            'adresy':adresy,
            'karty_płatnicze':kartyplatnicze,
            'adres_size':len(adresy),
            'karty_płatnicze_size':len(kartyplatnicze)
        })
        
    else:
        return redirect('sklep:base')

def add_adres(request):
    initialize(request)
    if request.method=='POST':
        adres_form=AdresForm(request.POST)
        if adres_form.is_valid():
            print("dodawanie adresu")
            adres=adres_form.save()
            adres.klient=Klient.objects.get(user=request.user)
            adres.imie=request.user.first_name
            adres.nazwisko=request.user.last_name
            adres.save()
            return redirect('sklep:user_view')
        else:
            return render(request,'sklep/user/user_adres.html',{
            'adres_form':adres_form,
            })
    else:
        if request.user.is_authenticated:
            adres_form=AdresForm()
        else:
            return redirect('sklep:base')

    return render(request,'sklep/user/user_adres.html',{
        'adres_form':adres_form,
    })

def egz_adres_modify_view(request,adres_id):
    initialize(request)
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
            return render(request,'sklep/user/user_egz_adres.html',{
            'adres_form':adres_form,
            'adres_id':adres.id,
            })
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

    initialize(request)
    adres=Adres.objects.get(id=adres_id)
    if request.method=='POST':
        adres.delete()
    return redirect('sklep:user_view')

def user_dat_mod(request):
    initialize(request)
    if request.user.is_authenticated:
        klient=Klient.objects.get(user=request.user)
        if request.method=='POST':
            user_form=UserDataModification(request.POST)
            klient_form=klientForm(request.POST)
            user_nick_form=UserNickMod(request.POST)
            isvalid=True
            userError='A user with that username already exists.'
            if user_nick_form.is_valid():
                klient.user.username=user_nick_form.cleaned_data['username']
            elif user_nick_form['username'].errors[0] in userError and klient.user.username==user_nick_form.data['username']:
                isvalid=True
                user_nick_form.errors.clear()
            else:
                isvalid=False
            if user_form.is_valid():
                print('zmieniam dane')
                klient.user.email=user_form.cleaned_data['email']
                klient.user.first_name=user_form.cleaned_data['first_name']
                klient.user.last_name=user_form.cleaned_data['last_name']
                klient.user.save()
            else:
                isvalid=False
                
            if klient_form.is_valid():
                print("form klient")
                klient.telefon=klient_form.cleaned_data['telefon']
                klient.data_urodzenia=klient_form.cleaned_data['data_urodzenia']
                klient.save()
            else:
                isvalid=False

            if isvalid==False:
                        return render(request,'sklep/user/user_dat_mod.html',{
                        'user_mod_form':user_form,
                        'klient_mod_form':klient_form,
                        'user_nick_form':user_nick_form,
                        })
            return redirect('sklep:user_view')
        else:
            user_nick_form=UserNickMod(initial={
                'username':klient.user.username,
            })
            user_form=UserDataModification(initial={
                #'username':klient.user.username,
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
        'klient_mod_form':klient_form,
        'user_nick_form':user_nick_form,
    })
    else:
        return redirect('sklep:base')

def zamowienie_szcz(request,id_zamowienia):
    initialize(request)
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

    
def filter_view(request,filter):
    initialize(request)
    
    produkt_list=[]
    try:
        kategoria=Kategoria.objects.get(nazwa=filter)

        try:
            podkategorie=Podkategoria.objects.filter(kategoria=kategoria)
        except:
            podkategorie=[]

        for podkategoria in podkategorie:
            print(podkategoria.nazwa)
            try:
                produkty=Produkt.objects.filter(podkategoria = podkategoria)
            except:
                produkty=[]
            produkt_list.extend(produkty)
    except:
        produkt_list=[]
    marki=[]
    for produkt in produkt_list:
        if not(produkt.marka in marki):
            marki.append(produkt.marka)

    color=request.GET.get('color')
    marka=request.GET.get('marka')
    podkategoria_nazwa=request.GET.get('podkategoria')
    cena_min=request.GET.get("cena_min")
    cena_max=request.GET.get("cena_max")

    if podkategoria_nazwa !='' and podkategoria_nazwa is not None:
        podkategoria=Podkategoria.objects.get(id=podkategoria_nazwa)
        lista_buf=[]
        for produkt in produkt_list:
            if podkategoria==produkt.podkategoria:
                lista_buf.append(produkt)
        produkt_list=lista_buf

    print(color)
    if color !='' and color is not None:
        lista_buf=[]
        for produkt in produkt_list:
            if color in produkt.opis:
                lista_buf.append(produkt)
        produkt_list=lista_buf

    print(marka)
    if marka !='' and marka is not None:
        lista_buf=[]
        for produkt in produkt_list:
            if marka == produkt.marka:
                lista_buf.append(produkt)
        produkt_list=lista_buf

    print(cena_min)
    if cena_min !='' and cena_min is not None:
        lista_buf=[]
        for produkt in produkt_list:
            if int(cena_min) <= produkt.cena:
                lista_buf.append(produkt)
        produkt_list=lista_buf

    print(cena_max)
    if cena_max !='' and cena_max is not None:
        lista_buf=[]
        for produkt in produkt_list:
            if int(cena_max) >= produkt.cena:
                lista_buf.append(produkt)
        produkt_list=lista_buf

    context = {
        'produkt_list' : produkt_list,
        'podkategorie':podkategorie,
        'marki': marki
    }
    return render(request, 'sklep/base/category.html',context)


def del_user(request, id):
    initialize(request)
    if request.user.is_authenticated:   
        try:
            a = User.objects.get(id = id)
            b = Klient.objects.get(user = a)
            a.delete()
            b.delete()
            messages.success(request, "Usunięto konto")            

        except User.DoesNotExist:
            messages.error(request, "Konto nie istnieje")    
            return redirect(request, 'sklep:base')

        except Exception as e: 
            return redirect(request, 'sklep:base',{'err':e.message})

        return redirect('sklep:base') 
    else:
        return redirect('sklep:base')

def del_user_page(request):
    initialize(request)
    return render(request,'sklep/user/user_del.html',{})


def add_credit_card(request):
    initialize(request)
    if request.method=='POST':
        kartyplatnicze_form=KartyPlatniczeForm(request.POST)
        if kartyplatnicze_form.is_valid():
            print("dodawanie karty płatniczej")
            kartyplatnicze=kartyplatnicze_form.save()
            kartyplatnicze.klient=Klient.objects.get(user=request.user)
            
            kartyplatnicze.save()
            return redirect('sklep:user_view')
        else:
            return render(request,'sklep/user/user_credit_card.html',{
            'kartyplatnicze_form':kartyplatnicze_form,
            })
    else:
        if request.user.is_authenticated:
            kartyplatnicze_form=KartyPlatniczeForm()
        else:
            return redirect('sklep:base')

    return render(request,'sklep/user/user_credit_card.html',{
        'kartyplatnicze_form':kartyplatnicze_form,
    })

def egz_credit_modify_view(request,kartyplatnicze_id):
    initialize(request)
    kartyplatnicze=KartyPlatnicze.objects.get(id=kartyplatnicze_id)
    if request.method=='POST':
        kartyplatnicze_form=KartyPlatniczeForm(request.POST)
        if kartyplatnicze_form.is_valid():
            print("modyfikowanie adresu")
            kartyplatnicze.numer=kartyplatnicze_form.cleaned_data['numer']
            kartyplatnicze.cvc=kartyplatnicze_form.cleaned_data['cvc']
            kartyplatnicze.miesiac=kartyplatnicze_form.cleaned_data['miesiac']
            kartyplatnicze.rok=kartyplatnicze_form.cleaned_data['rok']
            kartyplatnicze.save()
            return redirect('sklep:user_view')
        else:
            return render(request,'sklep/user/user_egz_credit.html',{
            'kartyplatnicze_form':kartyplatnicze_form,
            'kartyplatnicze_id':kartyplatnicze.id,
            })
    else:
        if request.user.is_authenticated:
            kartyplatnicze_form=KartyPlatniczeForm(initial={
                'numer':kartyplatnicze.numer,
                'cvc':kartyplatnicze.cvc,
                'miesiac':kartyplatnicze.miesiac,
                'rok':kartyplatnicze.rok,
            })
        else:
            return redirect('sklep:base')

    return render(request,'sklep/user/user_egz_credit.html',{
        'kartyplatnicze_form':kartyplatnicze_form,
        'kartyplatnicze_id':kartyplatnicze.id,
    })


def del_credit(request,kartyplatnicze_id):
    initialize(request)
    kartyplatnicze=KartyPlatnicze.objects.get(id=kartyplatnicze_id)
    if request.method=='POST':
        kartyplatnicze.delete()
    return redirect('sklep:user_view')

def kontakt(request):
    if request.user.is_authenticated:
        klient=Klient.objects.get(user=request.user)
        if request.method=='POST':
            wiadomosc=request.GET.get("temat")
            wiadomosc2=request.GET.get("treść")
            
            
            print(wiadomosc)
            print(wiadomosc2)
            if wiadomosc != '' and wiadomosc is not None and wiadomosc2 != '' and wiadomosc2 is not None:
                send_mail(wiadomosc,wiadomosc2,klient.user.email,
                ['tenobok54@gmail.com'],fail_silently=False,)
            return redirect('sklep:user_view')
            
        return render(request,'sklep/user/kontakt.html')
    else:
        return redirect('sklep:base')
    