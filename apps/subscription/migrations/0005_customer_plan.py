# Generated by Django 3.2.7 on 2021-10-20 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_auto_20211020_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='plan',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
