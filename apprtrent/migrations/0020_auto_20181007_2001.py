# Generated by Django 2.1.1 on 2018-10-07 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apprtrent', '0019_auto_20181005_0718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appartment',
            name='address_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apprtrent.City', verbose_name='miasto'),
        ),
    ]
