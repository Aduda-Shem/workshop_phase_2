# Generated by Django 4.2.3 on 2023-10-24 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_remove_historicalproduct_selling_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salerecord',
            name='selling_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
