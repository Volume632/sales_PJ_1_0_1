# Generated by Django 5.1 on 2024-09-10 10:43

import sales_project.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_project', '0003_alter_salesrecord_date_alter_salesrecord_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='salesrecord',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='stockrecord',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='salesfile',
            name='file',
            field=models.FileField(upload_to='sales_files/', validators=[sales_project.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='salesrecord',
            name='sale_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='salesrecord',
            name='total_price',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stockfile',
            name='file',
            field=models.FileField(upload_to='stock_files/', validators=[sales_project.models.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='supplierfile',
            name='file',
            field=models.FileField(upload_to='supplier_files/', validators=[sales_project.models.validate_file_extension]),
        ),
    ]
