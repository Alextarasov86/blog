# Generated by Django 4.1.3 on 2023-01-08 11:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_viewarticle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='view_count',
        ),
    ]
