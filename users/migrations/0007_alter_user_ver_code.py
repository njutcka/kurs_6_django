# Generated by Django 4.2.7 on 2023-12-15 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_is_activated_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ver_code',
            field=models.CharField(default='069796292307', max_length=15, verbose_name='Проверочный код'),
        ),
    ]
