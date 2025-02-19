# Generated by Django 5.1.6 on 2025-02-19 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='fine',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
    ]
