# Generated by Django 3.0.3 on 2020-02-10 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOPC_Reg_SYS', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allstudents',
            name='penalty',
            field=models.IntegerField(default=99999),
        ),
        migrations.AddField(
            model_name='allstudents',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='allstudents',
            name='shift',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='allstudents',
            name='solve',
            field=models.IntegerField(default=99),
        ),
        migrations.AddField(
            model_name='regstudents',
            name='password',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='regstudents',
            name='shift',
            field=models.CharField(default='Pending', max_length=100),
        ),
        migrations.AddField(
            model_name='regstudents',
            name='userid',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AlterField(
            model_name='regstudents',
            name='penalty',
            field=models.IntegerField(default=99999),
        ),
    ]