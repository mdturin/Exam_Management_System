# Generated by Django 4.0.5 on 2022-07-24 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_teacher_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='supervisor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='account.teacher'),
        ),
    ]
