# Generated by Django 2.0.13 on 2019-09-20 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0002_auto_20190919_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='title',
        ),
        migrations.AlterField(
            model_name='question',
            name='question_text',
            field=models.TextField(max_length=300),
        ),
    ]
