# Generated by Django 5.1.5 on 2025-01-28 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0004_transactionmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionmodel',
            name='type',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
