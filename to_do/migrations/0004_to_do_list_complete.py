# Generated by Django 4.2.16 on 2024-12-05 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_do', '0003_alter_to_do_list_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='to_do_list',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]