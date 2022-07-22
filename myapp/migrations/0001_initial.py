# Generated by Django 4.0.4 on 2022-05-10 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=10, unique=True, verbose_name='用户名')),
                ('password', models.IntegerField(max_length=10, verbose_name='密码')),
                ('user_type', models.IntegerField(choices=[(1, '管理员'), (2, '普通用户')], default=2, verbose_name='用户类型')),
            ],
        ),
    ]
