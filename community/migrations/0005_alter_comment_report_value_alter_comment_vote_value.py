# Generated by Django 4.0.5 on 2022-07-10 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0004_alter_post_report_value_alter_post_vote_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='report_value',
            field=models.IntegerField(choices=[('up', 'Reported'), ('down', 'Report')], default=0),
        ),
        migrations.AlterField(
            model_name='comment',
            name='vote_value',
            field=models.IntegerField(choices=[('up', 'UP VOTE'), ('up', 'DOWN VOTE')], default=0),
        ),
    ]