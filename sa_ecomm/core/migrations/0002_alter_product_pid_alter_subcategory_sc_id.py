# Generated by Django 4.2.3 on 2023-07-21 18:06

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=20, prefix='', unique=True),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='sc_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=10, max_length=20, prefix='scat', unique=True),
        ),
    ]
