# Generated by Django 3.0.4 on 2020-08-29 02:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=140)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_name', models.CharField(max_length=50)),
                ('user_id', models.BigIntegerField(primary_key=True, serialize=False, unique=True)),
                ('screen_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('secret_status', models.CharField(choices=[('1', '鍵垢'), ('0', '公開垢')], default='1', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Task_history',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tweet_id', models.BigIntegerField()),
                ('tweet_text', models.CharField(max_length=140)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('praised', models.BooleanField(default=False)),
                ('user_id', models.BigIntegerField()),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Task')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User'),
        ),
    ]
