# Generated by Django 4.0.5 on 2022-07-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_remove_comment_com_image_alter_comment_vote_value_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='report_value',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='vote_ratio',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='vote_total',
        ),
        migrations.AlterField(
            model_name='comment',
            name='vote_value',
            field=models.CharField(choices=[('up', 'UP VOTE'), ('up', 'DOWN VOTE')], max_length=200),
        ),
    ]