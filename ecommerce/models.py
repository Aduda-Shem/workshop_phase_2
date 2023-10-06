from django.db import models
from users.models import User
from simple_history.models import HistoricalRecords

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/')

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='subcategory_images/')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name

    def calculate_stock_in(self):
        sale_records = SaleRecord.objects.filter(product=self)
        stock_in = sum(record.quantity_sold for record in sale_records)
        return stock_in

    def calculate_stock_out(self):
        sale_records = SaleRecord.objects.filter(product=self)
        stock_out = sum(record.quantity_sold for record in sale_records)
        return stock_out

    @property
    def total_stock_quantity(self):
        stock_in = self.calculate_stock_in()
        stock_out = self.calculate_stock_out()
        total_stock = stock_in - stock_out
        return total_stock

class PointOfSale(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_datetime = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"POS-{self.id}"

class SaleRecord(models.Model):
    point_of_sale = models.ForeignKey(PointOfSale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SaleRecord-{self.id}"
