# Generated by Django 5.1 on 2024-09-10 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_project', '0004_product_updated_at_salesrecord_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesfile',
            name='file',
            field=models.FileField(upload_to='sales_files/'),
        ),
    ]
