# Generated by Django 3.2.12 on 2022-05-22 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_container_busy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task_node_wait',
            name='start_time',
            field=models.CharField(max_length=512, null=True),
        ),
    ]