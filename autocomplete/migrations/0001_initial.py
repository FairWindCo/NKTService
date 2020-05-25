# Generated by Django 2.1.7 on 2019-05-29 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutoComplete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=250, verbose_name='Наименование')),
                ('section', models.CharField(choices=[('ER', 'Варианты ошибок'), ('CM', 'Варианты комплектации'), ('DM', 'Документы')], max_length=2)),
            ],
            options={
                'verbose_name': 'Настройки автодополнения',
                'db_table': 'base_autocomplete',
                'ordering': ['text'],
            },
        ),
    ]
