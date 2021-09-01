# Generated by Django 3.2.6 on 2021-09-01 17:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('private', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('poster', models.ImageField(blank=True, null=True, upload_to='images/guilds/posters')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='guilds', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('banned', models.BooleanField(default=False)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='chat.guild')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons_messages', to='chat.member')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels_messages', to='chat.channel')),
            ],
        ),
        migrations.CreateModel(
            name='InviteLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=30, null=True, unique=True)),
                ('guild', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation_links', to='chat.guild')),
            ],
        ),
        migrations.AddField(
            model_name='channel',
            name='guild',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='channels', to='chat.guild'),
        ),
    ]