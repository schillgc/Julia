from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Phone(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        ordering = ['make', 'model']

    def __str__(self):
        return self.make + " " + self.model


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = PhoneNumberField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name + " " + self.last_name


class Discount(models.Model):
    name = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    users = models.ManyToManyField(User)
    expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['expires', 'name', 'amount']

    def __str__(self):
        return self.user.first_name + "\'s" + " " + self.name


class AdditionalTaxOrFee(models.Model):
    name = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    users = models.ManyToManyField(User)

    class Meta:
        ordering = ['name', 'amount']

    def __str__(self):
        return self.name + " for " + str(self.users.all())


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    is_leased = models.BooleanField(default=True)
    is_insured = models.BooleanField(default=True)
    cost_of_insurance = models.IntegerField(default=0, null=True)

    class Meta:
        ordering = ['is_active', 'user', 'phone']

    def is_leased(self):
        if self.is_leased:
            self.monthly_phone_cost = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.user)
