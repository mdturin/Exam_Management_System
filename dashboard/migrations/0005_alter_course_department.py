# Generated by Django 4.0.5 on 2022-06-30 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_course_credits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.department'),
        ),
    ]
