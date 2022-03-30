from django.db import models
from djmoney.models.fields import MoneyField


# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey('User')

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return False

    @staticmethod
    def has_write_permission(request):
        """
        We can remove the has_create_permission because this implicitly grants that permission.
        """
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    @staticmethod
    @authenticated_users
    def has_publish_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_publish_permission(self, request):
        return request.user == self.owner


class Product(models.Model):
    brand = models.CharField(max_length=200)
    item = models.CharField(max_length=1000)
    value = MoneyField(max_digits=17, decimal_places=2, default_currency='USD')
    quantity = models.IntegerField()

    class Meta:
        permissions = [
            ("read_product", "allow read operation for active products only"),
            ("manage_product", "CUD operations for active products"),
            ("admin",
             "read operation, list all products regardless of their status (active / deleted) - hard delete a product")
        ]

    def __str__(self):
        return str(self.quantity) + " " + self.brand + "'s " + self.item + " for " + str(self.value)
