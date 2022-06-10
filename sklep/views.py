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

from .forms import  ExtendedUserCreationForm,klientForm,UserDataModification,AdresForm
from .models import Adres, Platnosci, PozycjaZamowienia, Produkt, Opinie,Klient, RodzajePlatnosci, Zamowienie, RodzajWysylki,KartyPlatnicze
# Create your views here.

def base(request):
    produkt_list = Produkt.objects.all()
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
        opinie = Opinie.objects.all()
    except:
        raise Http404('Produkt nie istnieje, łooot?')
    return render(request, 'sklep/base/produkt-details.html',{
        'produkt' : produkt,
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
    pozycja_zamowienia = PozycjaZamowienia.objects.create(
        ilosc = request.POST['ilosc'], 
        produkt = produkt)
    klient_zamowienie, status = Zamowienie.objects.get_or_create(
        klient = klient,
        data_zamowienia = datetime.now()
        ,czy_zamowione = False)
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


#/////////////////////////////////////////////////////////////////////////////////////

def orders_view(request):
    if request.user.is_authenticated:
        try:
            zamowienia=Zamowienie.objects.get(klient=request.user.id)
        except:
            zamowienia=[]
            #return HttpResponse('nothing to show')
        #return HttpResponse(request.user.id)
        return render(request, 'sklep/user/orders_view.html',{
            'zamowienia':zamowienia
        })
    else:
        return render(request,'sklep/user/not_logged.html')
        #return render(request, 'sklep/user_view.html')

def user_view(request):
    if request.user.is_authenticated:
        try: 
            uzytkownik=Klient.objects.get(user=request.user.id)
        except:
            return Http404
        adresy=Adres.objects.filter(klient=request.user.id)
        return render(request,'sklep/user/user_view.html',{
            'data_ur':uzytkownik.data_urodzenia,
            'telefon':uzytkownik.telefon,
            'adresy':adresy,
            'adres_size':len(adresy)
        })
        
    else:
        return render(request,'sklep/user/not_logged.html')

def add_adres(request):
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
        if request.user.is_authenticated:
            adres_form=AdresForm()
        else:
            return render(request,'sklep/user/not_logged.html')

    return render(request,'sklep/user/user_adres.html',{
        'adres_form':adres_form,
    })

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
            return render(request,'sklep/user/not_logged.html')

    return render(request,'sklep/user/user_egz_adres.html',{
        'adres_form':adres_form,
        'adres_id':adres.id,
    })

def del_adres(request,adres_id):
    adres=Adres.objects.get(id=adres_id)
    if request.method=='POST':
        adres.delete()
    return redirect('sklep:user_view')