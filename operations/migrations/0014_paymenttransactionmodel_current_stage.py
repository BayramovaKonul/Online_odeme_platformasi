# Generated by Django 5.1 on 2025-02-03 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0013_remove_paymenttransactionmodel_prefix"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymenttransactionmodel",
            name="current_stage",
            field=models.IntegerField(default=0),
        ),
    ]
