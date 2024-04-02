# Generated by Django 5.0.3 on 2024-03-19 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('desc', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='image')),
            ],
        ),
    ]
