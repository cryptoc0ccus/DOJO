# Generated by Django 3.2.7 on 2021-10-17 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datatables', '0012_delete_guardian'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_ready',
            field=models.BooleanField(default=False),
        ),
    ]