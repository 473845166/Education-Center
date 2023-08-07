# Generated by Django 4.2.3 on 2023-08-07 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_record_submit_date_alter_openness_end_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='submit_date',
        ),
        migrations.AlterField(
            model_name='openness',
            name='end_time',
            field=models.TimeField(verbose_name='结束时间'),
        ),
        migrations.AlterField(
            model_name='openness',
            name='start_time',
            field=models.TimeField(verbose_name='开放时间'),
        ),
        migrations.AlterField(
            model_name='record',
            name='submit',
            field=models.DateTimeField(auto_now_add=True, verbose_name='请求预约时间'),
        ),
    ]
