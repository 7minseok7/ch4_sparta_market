# Generated by Django 4.2 on 2024-12-26 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goods',
            name='like_users',
            field=models.ManyToManyField(related_name='like_articles', to=settings.AUTH_USER_MODEL),
        ),
    ]
