# Generated by Django 4.2.7 on 2023-12-18 19:40

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("teams", "0007_remove_grouptransaction_timestamp_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="grouptransaction",
            old_name="user",
            new_name="from_user",
        ),
    ]