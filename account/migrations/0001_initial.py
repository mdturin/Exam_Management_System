# Generated by Django 4.0.5 on 2022-06-21 11:30

import account.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_alter_department_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Professor', 'Professor'), ('Associate Professor', 'Associate Professor'), ('Assistant Professor', 'Assistant Professor'), ('Lecturer', 'Lecturer'), ('None', 'None')], default='None', max_length=255)),
                ('contact_number', models.CharField(max_length=11, unique=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=account.models.get_profile_pictures_directory)),
                ('is_dean', models.BooleanField(default=False)),
                ('department', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='dashboard.department')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
