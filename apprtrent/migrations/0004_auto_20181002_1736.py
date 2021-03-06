# Generated by Django 2.1.1 on 2018-10-02 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apprtrent', '0003_auto_20181002_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appartment',
            name='best_app',
            field=models.BooleanField(default=True, help_text='czy apartament ma być pokazywany na stronie głóœnej', verbose_name='favourite'),
        ),
        migrations.AlterField(
            model_name='appartment',
            name='fees',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apprtrent.Fee', verbose_name='dodatkowe opłaty'),
        ),
    ]
