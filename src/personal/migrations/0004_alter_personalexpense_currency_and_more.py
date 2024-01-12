# Generated by Django 4.2.7 on 2024-01-08 13:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("personal", "0003_alter_personalexpense_date_alter_personalincome_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="personalexpense",
            name="currency",
            field=models.CharField(
                choices=[("$", "$")], default="$", max_length=3, verbose_name="currency"
            ),
        ),
        migrations.AlterField(
            model_name="personalincome",
            name="currency",
            field=models.CharField(
                choices=[("$", "$")], default="$", max_length=3, verbose_name="currency"
            ),
        ),
    ]
