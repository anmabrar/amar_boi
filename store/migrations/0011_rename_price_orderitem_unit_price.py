# Generated by Django 5.0.6 on 2024-05-30 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_cart_alter_book_author_cartitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='price',
            new_name='unit_price',
        ),
    ]
