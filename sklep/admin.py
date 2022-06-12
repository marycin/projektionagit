from django.contrib import admin

# Register your models here.

from .models import Klient, Adres, RodzajePlatnosci,Platnosci,Produkt,Zamowienie,RodzajWysylki,Pracownik,Opinie,Zdjecia,Kategoria,Podkategoria, PozycjaZamowienia, KartyPlatnicze, Rozmiar, Produkt_Rozmiar

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
admin.site.register(PozycjaZamowienia)
admin.site.register(Rozmiar)
admin.site.register(Produkt_Rozmiar)
admin.site.register(KartyPlatnicze)
