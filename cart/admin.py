from django.contrib import admin
from .models import *

admin.site.register(CartItem)
admin.site.register(Cart)
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    list_display = ("subject", "catalog_number", "instructor_name",)

admin.site.register(Course, CourseAdmin)