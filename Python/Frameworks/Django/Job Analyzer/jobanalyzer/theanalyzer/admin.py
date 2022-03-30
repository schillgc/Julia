from django.contrib import admin

from .models import Benefit, Company, Position, Recruiter

admin.site.register(Benefit)
admin.site.register(Company)
admin.site.register(Position)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('company' + 'title',)}


admin.site.register(Recruiter)
