# Generated by Django 5.1 on 2025-02-02 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0010_alter_transactionmodel_completed_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymenttransactionmodel",
            name="amount",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name="paymenttransactionmodel",
            name="value",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="paymenttransactionmodel",
            name="value_type",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
