# Generated by Django 4.2.3 on 2023-08-07 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_alter_record_submit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='reserve',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.openness', verbose_name='事件'),
        ),
        migrations.AlterField(
            model_name='record',
            name='submit',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
    ]
