# Generated by Django 3.2.7 on 2021-10-19 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datatables', '0016_student_guardians_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='is_ready',
            new_name='is_founder',
        ),
    ]