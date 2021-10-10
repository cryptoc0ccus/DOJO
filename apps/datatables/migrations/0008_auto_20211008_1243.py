# Generated by Django 3.2.7 on 2021-10-08 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datatables', '0007_remove_membership_membership_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
        migrations.AddField(
            model_name='student',
            name='is_kid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='is_teen',
            field=models.BooleanField(default=False),
        ),
    ]
