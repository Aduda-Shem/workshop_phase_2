# Generated by Django 4.2.3 on 2023-10-08 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_alter_historicalproduct_selling_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproduct',
            name='selling_price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='selling_price',
        ),
        migrations.AddField(
            model_name='salerecord',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
