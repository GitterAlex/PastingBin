# Generated by Django 2.1.7 on 2019-03-13 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostessPasties', '0006_auto_20190312_2211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttable',
            name='postID',
            field=models.CharField(default='ijddclnb', help_text='Unique ID for this post', max_length=8, primary_key=True, serialize=False),
        ),
    ]