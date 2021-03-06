# Generated by Django 3.2.12 on 2022-03-08 06:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(regex='\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b')], verbose_name='Email')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('role', models.CharField(choices=[('SU', 'Superuser'), ('US', 'User')], max_length=2, verbose_name='Role')),
                ('is_active', models.BooleanField(default=True, verbose_name='User account is active')),
                ('time_created', models.DateTimeField(auto_now_add=True, verbose_name='Time create')),
                ('time_updated', models.DateTimeField(auto_now=True, verbose_name='Time updated')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
