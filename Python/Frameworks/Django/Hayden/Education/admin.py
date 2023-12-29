"""
Django Admin Configuration
"""

from django.contrib import admin

from .models import Credit, Institution, Instructor


@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    """
    Django Admin Configuration for Credits
    """
    prepopulated_fields = {'slug': ('grade_level', 'name',)}


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    """
    Django Admin Configuration for Institutions
    """
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    """
    Django Admin Configuration for Instructors
    """
    prepopulated_fields = {'slug': ('first_name', 'last_name',)}


class ClassInstuctorsInline(admin.TabularInline):
    model = Credit
    readonly_fields = ('teacher')
    extra = 1