from distutils.command.upload import upload
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.


class Klient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    data_urodzenia = models.DateField(null=True,blank=True)
    telefon = models.CharField(max_length=9,null=True,blank=True)
    
    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"


class Pracownik(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    data_urodzenia = models.DateField(null=True,blank=True)
    telefon = models.CharField(max_length=9,null=True,blank=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Pracownik"
        verbose_name_plural = "Pracownicy"


class Adres(models.Model):
    miejscowosc = models.CharField(max_length=50)
    ulica = models.CharField(max_length=50, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=6)
    numer_domu = models.CharField(max_length=5)
    numer_lokalu = models.IntegerField(blank=True,null=True)
    imie = models.CharField(max_length=50,blank=True,null=True)
    nazwisko = models.CharField(max_length=50,blank=True,null=True)
    klient = models.ForeignKey(Klient,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.miejscowosc, self.ulica, self.numer_domu}'

    class Meta:
        verbose_name = "Adres"
        verbose_name_plural = "Adresy"


class Podkategoria(models.Model):
    nazwa = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Podkategoria"
        verbose_name_plural = "Podkategorie"

    def __str__(self):
        return f"{self.nazwa}"



class Kategoria(models.Model):
    nazwa = models.CharField(max_length=50)
    podkategoria = models.ForeignKey('Podkategoria', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

    def __str__(self):
        return f"{self.nazwa}"


class Opinie(models.Model):
    komentarz = models.CharField(max_length=400)
    ocena = models.IntegerField()
    produkt = models.ForeignKey('Produkt',on_delete=models.CASCADE, null=True)
    klient = models.ForeignKey('Klient',on_delete=models.CASCADE, null=True)
    #usera jakos polacz

    class Meta:
        verbose_name = "Opinia"
        verbose_name_plural = "Opinie"
    
    def __str__(self):
        return f"{self.klient.user.username} {self.produkt.nazwa} {self.ocena}"


class Zdjecia(models.Model):
    zdjecie = models.ImageField(upload_to = 'images',null=True) #sciezka w staticu, poczytaj jeszcze

    class Meta:
        verbose_name = "Zdjecie"
        verbose_name_plural = "Zdjecia"


class Produkt(models.Model):
    nazwa = models.CharField(max_length=50)
    cena = models.DecimalField(max_digits=9,decimal_places=2)
    opis = models.CharField(max_length=500, blank=True)
    ilosc_dostepnego = models.PositiveIntegerField()
    zdjecia = models.ForeignKey('Zdjecia',on_delete=models.CASCADE,null=True)
    podkategoria = models.ForeignKey('Podkategoria',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.nazwa}"

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"


class Zamowienie(models.Model):
    data_zamowienia = models.DateField()
    data_wyslania = models.DateField()
    data_dostarczenia = models.DateField()
    czy_oplacono = models.BooleanField()
    adres = models.ForeignKey(Adres,on_delete=models.CASCADE)
    klient = models.ForeignKey(Klient,on_delete=models.CASCADE,null=True,blank=True)
    rodzaj_wysylki = models.ForeignKey('RodzajWysylki',on_delete=models.CASCADE,null=True)
    produkt = models.ManyToManyField('Produkt')

    def __str__(self):
        return f"{self.pk} {self.data_zamowienia}"

    class Meta:
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"

class RodzajWysylki(models.Model):
    nazwa = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.nazwa}"

    class Meta:
        verbose_name = "Rodzaj Wysyłki"
        verbose_name_plural = "Rodzaje Wysyłki"


class RodzajePlatnosci(models.Model):
    nazwa = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nazwa}"

    class Meta:
        verbose_name = "Rodzaje Platnosci"
        verbose_name_plural = "Rodzaje Platnosci"

class Platnosci(models.Model):
    kwota = models.DecimalField(max_digits=9,decimal_places=2)
    data_zaksiegowania = models.DateTimeField()
    rodzaj_platnosci = models.ForeignKey(RodzajePlatnosci,on_delete=models.CASCADE,null=True,blank=True)
    zamowienie = models.OneToOneField(Zamowienie,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.pk} {self.kwota} {self.data_zaksiegowania}"

    class Meta:
        verbose_name = "Płatności"
        verbose_name_plural = "Płatności"    

