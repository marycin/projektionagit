from email import message
from lib2to3.pgen2.token import OP
from mimetypes import common_types
from multiprocessing import context
from django.http import Http404,HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import  ExtendedUserCreationForm,klientForm,UserDataModification,AdresForm
from .models import Produkt, Opinie,Klient,Zamowienie,Adres
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