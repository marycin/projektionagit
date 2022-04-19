from mimetypes import common_types
from multiprocessing import context
from django.http import Http404
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


from .forms import  ExtendedUserCreationForm,klientForm
from .models import Produkt
# Create your views here.

def index(request):
    latest_produkt_list = Produkt.objects.order_by('cena')[:5]
    context = {'latest_produkt_list' : latest_produkt_list}
    return render(request, 'sklep/index.html',context)

def detail(request, produkt_id):
    try:
        produkt = Produkt.objects.get(pk = produkt_id)
    except Produkt.DoesNotExist:
        raise Http404('Produkt nie istnieje, łooot?')
    return render(request, 'sklep/detail.html',{
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
    else:
        form = ExtendedUserCreationForm(request.POST)
        klient_form = klientForm(request.POST)
    context = {
        'form' : form,
        'klient_form' : klient_form
    }
    return render(request, 'sklep/registration/register.html', context)

def login_user(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        print('eluwens')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.success(request,("There was an error, try again"))
            return redirect('login_user')
    
    return render(request, 'sklep/registration/login_user.html', {})
    #logowanie dziala, ale strona nie chce sie przekierowac po zalogowaniu, chuj wie dlaczego? ŁOT