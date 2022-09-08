from django.contrib import admin

from .models import User, Phone, Account, AdditionalTaxOrFee, Discount


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ['first_name', 'last_name']


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    ordering = ['make', 'model']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    ordering = ['users', 'name']


@admin.register(AdditionalTaxOrFee)
class AdditionalTaxOrFeeAdmin(admin.ModelAdmin):
    ordering = ['users', 'name', 'amount']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    ordering = ['user']
