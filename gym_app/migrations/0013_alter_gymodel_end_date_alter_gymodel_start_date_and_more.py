# Generated by Django 5.0.3 on 2024-04-10 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0012_gymodel_previous_data_alter_gymodel_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gymodel',
            name='end_date',
            field=models.CharField(default='1403-02-21', max_length=10),
        ),
        migrations.AlterField(
            model_name='gymodel',
            name='start_date',
            field=models.CharField(default='1403-01-22', max_length=10),
        ),
        migrations.AlterField(
            model_name='gymodel',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
