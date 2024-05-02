# Generated by Django 5.0.4 on 2024-05-02 05:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_item_country_item_customer_email_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='shop_name',
        ),
        migrations.AddField(
            model_name='item',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shop', to=settings.AUTH_USER_MODEL),
        ),
    ]
