# Generated by Django 4.1.3 on 2022-12-27 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_rename_sub_category_category_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
