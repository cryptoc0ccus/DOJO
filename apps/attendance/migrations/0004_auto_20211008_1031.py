# Generated by Django 3.2.7 on 2021-10-08 10:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datatables', '0004_auto_20210926_1104'),
        ('attendance', '0003_auto_20210919_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendancelist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('student', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='datatables.student')),
            ],
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]
