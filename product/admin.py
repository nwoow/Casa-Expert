from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(ServiceProduct)

class SubCategoryImageAdmin(admin.StackedInline):
    model = SubCategoryImage

class SubCategoryAdmin(admin.ModelAdmin):
    # list_display = ['subcategory']
    inlines = [SubCategoryImageAdmin]

admin.site.register(SubCategory,SubCategoryAdmin)
admin.site.register(Product)
admin.site.register(TimeSlot)

admin.site.register(CityService)