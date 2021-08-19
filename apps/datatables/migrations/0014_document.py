# Generated by Django 3.2.6 on 2021-08-17 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datatables', '0013_auto_20210816_2119'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='mydocs/', verbose_name='Document')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datatables.student')),
            ],
        ),
    ]