# Generated by Django 4.0.5 on 2022-06-21 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('facutly', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='dashboard.faculty')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('credits', models.FloatField()),
                ('code', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1', max_length=1)),
                ('semester', models.CharField(choices=[('I', 'I'), ('II', 'II')], default='I', max_length=2)),
                ('is_sessional', models.BooleanField(default=False)),
                ('department', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.department')),
            ],
        ),
    ]