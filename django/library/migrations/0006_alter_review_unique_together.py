# Generated by Django 5.1.6 on 2025-03-12 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0005_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('user', 'book')},
        ),
    ]
