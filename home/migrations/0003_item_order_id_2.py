# Generated by Django 5.0.4 on 2024-04-29 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_item_revenue_alter_item_shop_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='order_id_2',
            field=models.CharField(default=123, max_length=100),
            preserve_default=False,
        ),
    ]
