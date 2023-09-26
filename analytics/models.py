from django.db import models
from inventory.models import Category

from users.models import User

# Create your models here.

class SaleAnalytics(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_sales = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    average_sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale Analytics for {self.employee.username} in {self.category.name}"


class EmployeePerformance(models.Model):
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    total_sales = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    best_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Performance for {self.employee.username}"
