from distutils.command.upload import upload
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator


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
    numer_lokalu = models.CharField(max_length = 5, blank=True,null=True)
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
    kategoria = models.ForeignKey('Kategoria', on_delete=models.CASCADE,null=True)
    class Meta:
        verbose_name = "Podkategoria"
        verbose_name_plural = "Podkategorie"

    def __str__(self):
        return f"{self.nazwa} {self.kategoria.nazwa}"



class Kategoria(models.Model):
    nazwa = models.CharField(max_length=50)
    

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

    class Meta:
        verbose_name = "Opinia"
        verbose_name_plural = "Opinie"
    
    def __str__(self):
        return f"{self.klient.user.username} {self.produkt.marka} {self.produkt.model} {self.ocena}"


class Zdjecia(models.Model):
    zdjecie = models.ImageField(upload_to = 'images',null=True) #sciezka w staticu, poczytaj jeszcze
    produkt = models.ForeignKey('Produkt',on_delete=models.CASCADE,null=True)
    class Meta:
        verbose_name = "Zdjecie"
        verbose_name_plural = "Zdjecia"

class Rozmiar(models.Model):
    rozmiar = models.CharField(max_length=5)

    class Meta:
        verbose_name = "Rozmiar"
        verbose_name_plural = "Rozmiary"
    
    def __str__(self):
        return f"{self.rozmiar}"

class Produkt_Rozmiar(models.Model):
    ilosc_dostepnego = models.PositiveIntegerField()
    produkt = models.ForeignKey('Produkt',on_delete=models.CASCADE,null=True)
    rozmiar = models.ForeignKey('Rozmiar',on_delete=models.CASCADE,null=True)
    
    class Meta:
        verbose_name = "Produkt_Rozmiar"
        verbose_name_plural = "Produkty i rozmiary"
    
    def __str__(self):
        return f"{self.rozmiar.rozmiar} {self.produkt.marka} {self.produkt.model}"

class Produkt(models.Model):
    marka = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    cena = models.DecimalField(max_digits=9,decimal_places=2)
    opis = models.CharField(max_length=500, blank=True)
    zdjecie_glowne = models.ImageField(upload_to = 'images',null=True)
    podkategoria = models.ForeignKey('Podkategoria',on_delete=models.CASCADE,null=True)


    def __str__(self):
        return f"{self.marka} {self.model}"

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"


class PozycjaZamowienia(models.Model):
    ilosc = models.IntegerField()
    czy_zamowiony = models.BooleanField(default=False)
    data_dodania = models.DateTimeField(auto_now=True)
    data_zamowienia = models.DateTimeField(null=True)
    produkt = models.ForeignKey('Produkt', on_delete=models.CASCADE, null=True)
    rozmiar = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.produkt.marka} {self.produkt.model} {self.ilosc} {self.data_dodania}"
    
    class Meta:
        verbose_name = "Pozycja zamówienia"
        verbose_name_plural = "Pozycje zamówień"

class Zamowienie(models.Model):
    pozycje_zamowienia = models.ManyToManyField(PozycjaZamowienia)
    data_zamowienia = models.DateField()
    data_wyslania = models.DateField(null=True)
    data_dostarczenia = models.DateField(null=True)
    czy_zamowione = models.BooleanField(default=False)
    czy_oplacono = models.BooleanField(default=False)
    adres = models.ForeignKey(Adres,on_delete=models.CASCADE,null=True)
    klient = models.ForeignKey(Klient,on_delete=models.CASCADE,null=True,blank=True)
    rodzaj_wysylki = models.ForeignKey('RodzajWysylki',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.klient.user.first_name} {self.klient.user.last_name} {self.data_zamowienia}"

    def get_pozycje_zamowienia(self):
        return self.pozycje_zamowienia.all()

    def czy_puste(self):
        if self.pozycje_zamowienia.all() is None:
            return True
        else:
            return False

    def get_kwota_zamowienia(self):
        return sum([pozycja_zamowienia.produkt.cena * pozycja_zamowienia.ilosc for pozycja_zamowienia in self.pozycje_zamowienia.all()])

    class Meta:
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"


class RodzajWysylki(models.Model):
    nazwa = models.CharField(max_length=50)
    cena = models.DecimalField(max_digits=9,decimal_places=2)
    
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


class KartyPlatnicze(models.Model):
    numer = models.CharField(validators=[RegexValidator(regex='^.{16}$', message='Zły numer', code='nomatch')], max_length=16)
    cvc = models.CharField(validators=[RegexValidator(regex='^.{3}$', message='Zły numer', code='nomatch')], max_length=3)
    miesiac = models.CharField(max_length=2)
    rok = models.CharField(max_length=2)
    klient = models.ForeignKey('Klient',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.klient.user.first_name} {self.klient.user.last_name} {self.numer}"

    class Meta:
        verbose_name = "Karta Płatnicza"
        verbose_name_plural = "Karty Płatnicze"


class Platnosci(models.Model):
    kwota = models.DecimalField(max_digits=9,decimal_places=2)
    data_zaksiegowania = models.DateTimeField(null=True)
    rodzaj_platnosci = models.ForeignKey(RodzajePlatnosci,on_delete=models.CASCADE,null=True,blank=True)
    zamowienie = models.OneToOneField(Zamowienie,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.zamowienie.klient.user.first_name} {self.zamowienie.klient.user.last_name} {self.kwota} {self.data_zaksiegowania}"

    class Meta:
        verbose_name = "Płatności"
        verbose_name_plural = "Płatności"    