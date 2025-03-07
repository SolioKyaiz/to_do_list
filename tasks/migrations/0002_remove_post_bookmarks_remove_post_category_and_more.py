# Generated by Django 5.1.6 on 2025-03-03 11:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='bookmarks',
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.RemoveField(
            model_name='post',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='owner',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название задачи')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание задачи')),
                ('priority', models.CharField(choices=[('low', 'Низкий'), ('medium', 'Средний'), ('high', 'Высокий')], default='medium', max_length=10, verbose_name='Приоритет')),
                ('deadline', models.DateTimeField(verbose_name='Дедлайн')),
                ('status', models.CharField(choices=[('todo', 'To Do'), ('in_progress', 'In Progress'), ('in_review', 'In Review'), ('done', 'Done')], default='todo', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('category', models.ManyToManyField(related_name='tasks', to='tasks.category', verbose_name='Категории')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
