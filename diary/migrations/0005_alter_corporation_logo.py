# Generated by Django 3.2.5 on 2021-07-27 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0004_alter_corporation_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporation',
            name='logo',
            field=models.ImageField(null=True, upload_to='logos'),
        ),
    ]
