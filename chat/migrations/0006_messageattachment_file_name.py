# Generated by Django 4.2.1 on 2023-07-07 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_alter_messageattachment_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='messageattachment',
            name='file_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]