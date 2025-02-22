# Generated by Django 5.1 on 2025-02-06 10:07

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("operations", "0016_paymenttransactionmodel_transaction_type_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transaction_id",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                (
                    "account_number",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                (
                    "amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending_account", "Pending Account"),
                            ("pending_amount", "Pending Amount"),
                            ("pending_confirmation", "Pending Confirmation"),
                            ("completed", "Completed"),
                        ],
                        default="pending_account",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name="paymenttransactionmodel",
            name="transaction_type",
            field=models.CharField(max_length=50),
        ),
    ]
