# Generated by Django 4.0.5 on 2022-06-30 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_rename_facutly_department_faculty'),
        ('account', '0006_rename_facutly_routine_faculty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.faculty'),
        ),
    ]