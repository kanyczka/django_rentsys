# Generated by Django 2.1.1 on 2018-10-02 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apprtrent', '0005_auto_20181002_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='e_mail',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='owner',
            name='tel_no',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Nr telefonu'),
        ),
    ]
