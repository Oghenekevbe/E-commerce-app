# Generated by Django 3.2.16 on 2023-04-07 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0032_alter_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Phone Number'),
        ),
    ]
