# Generated by Django 2.1.7 on 2019-03-14 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HostessPasties', '0010_auto_20190313_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttable',
            name='postID',
            field=models.CharField(default='pvlzs1ot', help_text='Unique ID for this post', max_length=8, primary_key=True, serialize=False),
        ),
    ]