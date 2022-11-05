from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CartItem)
admin.site.register(Cart)

class CourseAdmin(admin.ModelAdmin):
    list_display = ("subject", "catalog_number", "instructor_name",)

admin.site.register(Course, CourseAdmin)

