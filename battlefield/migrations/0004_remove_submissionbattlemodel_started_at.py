# Generated by Django 5.1 on 2024-08-11 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('battlefield', '0003_rename_b_id_submissionbattlemodel_room_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissionbattlemodel',
            name='started_at',
        ),
    ]
