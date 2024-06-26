# Generated by Django 5.0.3 on 2024-04-04 18:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_remove_post_image_alter_postsphoto_post'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postsphoto',
            options={'verbose_name': 'Зображення', 'verbose_name_plural': 'Зображення'},
        ),
        migrations.AlterField(
            model_name='postsphoto',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.post', verbose_name='Пост'),
        ),
        migrations.AlterField(
            model_name='profile_wer',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to=settings.AUTH_USER_MODEL),
        ),
    ]
