from django.contrib import admin

# Register your models here.

from .models import Klient, Adres, RodzajePlatnosci,Platnosci,Produkt,Zamowienie,RodzajWysylki,Pracownik

admin.site.register(Klient)
admin.site.register(Adres)
admin.site.register(Platnosci)
admin.site.register(RodzajePlatnosci)
admin.site.register(Produkt)
admin.site.register(Zamowienie)
admin.site.register(RodzajWysylki)
admin.site.register(Pracownik)
