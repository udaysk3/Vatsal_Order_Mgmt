# Generated by Django 5.0.4 on 2024-05-02 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('employee', 'Employee'), ('manufacturer', 'Manufacturer'), ('admin', 'Admin'), ('shop', 'Shop')], default='employee', max_length=100),
        ),
    ]
