from django.contrib import admin

from .models import Credit, Institution, Instructor

# admin.site.register(Credit)
@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('grade_level', 'name',)}

# admin.site.register(Institution)
@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# admin.site.register(Instructor)
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('first_name', 'last_name',)}

class ClassInstuctorsInline(admin.TabularInline):
    model = Credit
    readonly_fields = ('teacher')
    extra = 1
