# Generated by Django 4.2.5 on 2023-09-29 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Distribuidora', '0005_alter_venta_cantidad_compra'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Venta',
        ),
    ]
