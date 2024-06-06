from rest_framework import serializers
from . models import *


class CategoryModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ="__all__"


class ServiceProductModelSerializers(serializers.ModelSerializer):
    product = serializers.CharField(source='product.product_name')
    category = serializers.CharField(source='category.category_name')
    product_image = serializers.CharField(source='product.image.url')
    subcat_uid = serializers.CharField(source='product.sub_category.uid')
    class Meta:
        model = ServiceProduct
        fields ="__all__"


class ServiceModelSerializers(serializers.ModelSerializer):
    service_product = ServiceProductModelSerializers(source='servicetype',
        many=True,
        read_only=True,
    )
    
    class Meta:
        model = Service
        fields ="__all__"


class SubCategoryImageModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = SubCategoryImage
        fields ="__all__"



class TimeSlotMModelSerializers(serializers.ModelSerializer):
    start_time=serializers.TimeField(format='%I:%M %p')
    end_time=serializers.TimeField(format='%I:%M %p')
    available = serializers.BooleanField(read_only=True)
    class Meta:
        model = TimeSlot
        fields = "__all__"


class SubCategoryModelSerializers(serializers.ModelSerializer):
    all_images = SubCategoryImageModelSerializers(source='subcategory_images',
        many=True,
        read_only=True,
    )
    category = serializers.CharField(source='category.category_name')
    class Meta:
        model = SubCategory
        fields = "__all__"


class ProductModelSerializers(serializers.ModelSerializer):
    subcat_uid = serializers.CharField(source='sub_category.uid')
    class Meta:
        model = Product
        fields ="__all__"