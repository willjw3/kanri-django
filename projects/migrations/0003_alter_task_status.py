# Generated by Django 3.2.7 on 2021-09-30 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20210930_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('TODO', 'todo'), ('IN PROGRESS', 'in progress'), ('CLOSED', 'closed')], default='OPEN', max_length=20),
        ),
    ]
