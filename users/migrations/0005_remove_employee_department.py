# Generated by Django 4.2.3 on 2023-10-02 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_employee_national_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='department',
        ),
    ]
