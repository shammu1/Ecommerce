# Generated by Django 4.2.3 on 2023-09-07 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_paid_status_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default='1.99', max_digits=9999999999),
        ),
    ]
