# Generated by Django 4.1.5 on 2023-02-16 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labels',
            name='name',
            field=models.CharField(max_length=150, null=True, unique=True),
        ),
    ]
