# Generated by Django 2.2 on 2021-01-23 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fan_apps', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selfgoal',
            name='hero',
        ),
        migrations.RemoveField(
            model_name='selfgoal',
            name='rogue',
        ),
        migrations.RemoveField(
            model_name='selfgoal',
            name='villain',
        ),
        migrations.DeleteModel(
            name='Rogue',
        ),
        migrations.DeleteModel(
            name='SelfGoal',
        ),
        migrations.DeleteModel(
            name='Villain',
        ),
    ]