# Generated by Django 3.2.16 on 2023-03-18 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20230318_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingaddress',
            name='date_added',
            field=models.DateTimeField(),
        ),
    ]
