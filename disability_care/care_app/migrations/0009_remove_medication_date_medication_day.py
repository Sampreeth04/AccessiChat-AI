# Generated by Django 5.0.2 on 2024-02-25 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('care_app', '0008_alter_medication_patient_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medication',
            name='date',
        ),
        migrations.AddField(
            model_name='medication',
            name='day',
            field=models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], default='', max_length=20),
            preserve_default=False,
        ),
    ]