# Generated by Django 4.2.7 on 2023-12-18 19:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("teams", "0005_teamexpense_users_settled"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grouptransaction",
            name="text",
            field=models.TextField(blank=True, max_length=20000, null=True),
        ),
        migrations.DeleteModel(
            name="TeamMember",
        ),
    ]
