# Generated by Django 4.0.3 on 2022-06-02 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sklep', '0007_remove_pozycjazamowienia_produkt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produkt',
            name='pozycja_zamowienia',
        ),
        migrations.AddField(
            model_name='pozycjazamowienia',
            name='produkt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sklep.produkt'),
        ),
    ]
