# Generated by Django 3.2.7 on 2021-10-08 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatables', '0006_membership_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='membership_status',
        ),
    ]
