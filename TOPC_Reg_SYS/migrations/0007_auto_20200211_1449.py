# Generated by Django 3.0.3 on 2020-02-11 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOPC_Reg_SYS', '0006_allstudents_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='allstudents',
            name='gender',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='regstudents',
            name='gender',
            field=models.CharField(default='none', max_length=100),
        ),
    ]
