# Generated by Django 4.0.5 on 2022-07-24 12:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_routine_examiners_alter_routine_supervisor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='supervisor', to='account.teacher'),
        ),
    ]
