# Generated by Django 3.2.16 on 2023-03-08 11:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20230308_1234'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False, null=True)),
                ('transaction_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.customer')),
            ],
        ),
        migrations.RenameModel(
            old_name='CartItem',
            new_name='OrderItem',
        ),
        migrations.DeleteModel(
            name='OrderCart',
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.order'),
        ),
    ]