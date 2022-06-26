from datetime import datetime
from itertools import product
from sklep.models import Klient
from django.contrib.auth.models import User
from django import forms  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.utils.translation import gettext_lazy as _


from .models import Klient, Opinie,Adres,KartyPlatnicze

lata = range(1900,int(datetime.now().year)+1)

class klientForm(forms.ModelForm):
    data_urodzenia = forms.DateField(widget=forms.SelectDateWidget(years=lata))
    class Meta:
        model = Klient
        fields =('telefon','data_urodzenia')

class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')

    def save(self, commit=True):
        user = super(ExtendedUserCreationForm, self).save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user

class opinieForm(forms.ModelForm):
    class Meta:
        model = Opinie
        fields =('komentarz', 'ocena','produkt','klient')

class UserDataModification(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('email','first_name','last_name')#'username',

class AdresForm(forms.ModelForm):
    class Meta:
        model=Adres
        fields=('miejscowosc','ulica','kod_pocztowy','numer_domu','numer_lokalu')

class UserNickMod(forms.ModelForm):
    class Meta:
        model=User
        fields=('username',)
        
class KartyPlatniczeForm(forms.ModelForm):
    class Meta:
        model=KartyPlatnicze
        fields=('numer','cvc','miesiac','rok')