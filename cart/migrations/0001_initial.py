# Generated by Django 4.1.1 on 2022-11-07 05:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instructor_name', models.CharField(default='', max_length=150)),
                ('instructor_email', models.EmailField(default='sample@email.com', max_length=254)),
                ('course_number', models.PositiveIntegerField(default=0)),
                ('course_section', models.CharField(default='', max_length=8)),
                ('subject', models.CharField(default='', max_length=5)),
                ('catalog_number', models.CharField(default='', max_length=7)),
                ('description', models.TextField(default='', max_length=254)),
                ('units', models.CharField(default='', max_length=10)),
                ('component', models.CharField(default='', max_length=10)),
                ('class_capacity', models.PositiveIntegerField(default=0)),
                ('wait_list', models.PositiveIntegerField(default=0)),
                ('wait_cap', models.PositiveIntegerField(default=0)),
                ('enrollment_total', models.PositiveIntegerField(default=0)),
                ('enrollment_available', models.PositiveIntegerField(default=0)),
                ('topic', models.TextField(default='', max_length=254)),
                ('days', models.CharField(default='', max_length=25)),
                ('start_time', models.TimeField(default=django.utils.timezone.now)),
                ('end_time', models.TimeField(default=django.utils.timezone.now)),
                ('facility_description', models.TextField(default='', max_length=254)),
            ],
            options={
                'verbose_name_plural': 'courses',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deptJson', models.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_units', models.PositiveIntegerField(default=0)),
                ('courses', models.ManyToManyField(to='cart.cartitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
