# Generated by Django 3.2.7 on 2021-10-20 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_alter_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='last4',
            field=models.CharField(max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='mandate_ref',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
