# Generated by Django 4.1.3 on 2022-12-02 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0002_albumrated_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albumrated',
            name='Image',
            field=models.ImageField(upload_to='profile_pics'),
        ),
    ]
