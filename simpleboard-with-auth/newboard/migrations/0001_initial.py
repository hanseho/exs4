# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=200)),
                ('content', models.TextField(verbose_name='contents', default='')),
                ('written_date', models.DateTimeField(verbose_name='written date', auto_now_add=True)),
                ('update_date', models.DateTimeField(verbose_name='update date', auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=200)),
                ('created_date', models.DateTimeField(verbose_name='written date', auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('content', models.TextField(verbose_name='reply')),
                ('written_date', models.DateTimeField(verbose_name='written_date', auto_now_add=True)),
                ('article', models.ForeignKey(to='newboard.Article')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='article',
            name='board',
            field=models.ForeignKey(to='newboard.Board'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
