# Generated by Django 3.2 on 2021-04-25 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0005_link_phno'),
    ]

    operations = [
        migrations.AddField(
            model_name='link',
            name='email',
            field=models.EmailField(blank=True, max_length=250),
        ),
    ]
