# Generated by Django 5.0.2 on 2024-03-17 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_content_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.URLField(default='http://placehold.it/900x300'),
        ),
    ]
