# Generated by Django 3.2.7 on 2021-10-15 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datatables', '0009_alter_membership_autorenew_membership'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=30, null=True, verbose_name='First name')),
                ('last_name', models.CharField(default='', max_length=30, null=True, verbose_name='Last name')),
                ('phone', models.CharField(default='', max_length=30, null=True, verbose_name='Phone')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='datatables.student')),
            ],
        ),
    ]
