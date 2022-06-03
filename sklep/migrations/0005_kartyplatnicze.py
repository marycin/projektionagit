# Generated by Django 4.0.3 on 2022-06-02 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sklep', '0004_alter_zamowienie_adres'),
    ]

    operations = [
        migrations.CreateModel(
            name='KartyPlatnicze',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numer', models.CharField(max_length=16)),
                ('cvc', models.CharField(max_length=3)),
                ('miesiac', models.CharField(max_length=2)),
                ('rok', models.CharField(max_length=2)),
                ('klient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sklep.klient')),
            ],
        ),
    ]
