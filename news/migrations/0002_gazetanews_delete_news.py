# Generated by Django 5.2.3 on 2025-07-03 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GazetaNews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('image', models.URLField(blank=True, null=True)),
                ('full_text', models.TextField()),
                ('time_ago', models.CharField(max_length=50)),
                ('link', models.URLField(unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='News',
        ),
    ]
