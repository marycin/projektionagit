from email import message
from mimetypes import common_types
from multiprocessing import context
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import  ExtendedUserCreationForm,klientForm,UserDataModification
from .models import Produkt, Zamowienie,Klient,Adres
# Create your views here.

def base(request):
    latest_produkt_list = Produkt.objects.order_by('cena')[:5]
    context = {'latest_produkt_list' : latest_produkt_list}
    return render(request, 'sklep/base.html',context)

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
    except:
        raise Http404('Produkt nie istnieje, łooot?')
    return render(request, 'sklep/base/base__produkt-details.html',{
        'produkt' : produkt
    })

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
    return render(request, 'sklep/registration/register.html', context)

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
    
    return render(request, 'sklep/registration/login_user.html', {})
    #tylko admin moze sie logowac, zmien potem nazwe na login

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
        return render(request, 'sklep/orders_view.html',{
            'zamowienia':zamowienia
        })
    else:
        return render(request,'sklep/registration/not_logged.html')
        #return render(request, 'sklep/user_view.html')

def user_view(request):
    if request.user.is_authenticated:
        try: 
            uzytkownik=Klient.objects.get(user=request.user.id)
        except:
            return Http404
        try:
            adresy=Adres.object.get(klient=request.user.id)
        except:
            adresy=[]
        return render(request,'sklep/user_view.html',{
            'data_ur':uzytkownik.data_urodzenia,
            'telefon':uzytkownik.telefon,
            'adresy':adresy,
            'adres_size':len(adresy)
        })
        
    else:
        return render(request,'sklep/registration/not_logged.html')

def user_modify_view(request):
    user_mod_form=UserDataModification()
    return HttpResponse('strona adres')