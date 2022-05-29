from django.contrib import admin

# Register your models here.

from .models import Klient, Adres, RodzajePlatnosci,Platnosci,Produkt,Zamowienie,RodzajWysylki,Pracownik,Opinie,Zdjecia,Kategoria,Podkategoria

admin.site.register(Klient)
admin.site.register(Adres)
admin.site.register(Platnosci)
admin.site.register(RodzajePlatnosci)
admin.site.register(Produkt)
admin.site.register(Zamowienie)
admin.site.register(RodzajWysylki)
admin.site.register(Pracownik)
admin.site.register(Opinie)
admin.site.register(Zdjecia)
admin.site.register(Kategoria)
admin.site.register(Podkategoria)
