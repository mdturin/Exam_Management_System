# Generated by Django 4.0.5 on 2022-07-24 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_routine_supervisor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routine',
            name='examiners',
        ),
        migrations.AddField(
            model_name='routine',
            name='examiners',
            field=models.ManyToManyField(related_name='+', to='account.teacher'),
        ),
    ]
