from django.db import models
from base.models import BaseModel
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg
# Create your models here.


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)
    is_publish = models.BooleanField(default=True)
    category_image = models.ImageField(upload_to='categories')

    def save(self,*arg,**kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*arg,**kwargs)

    def __str__(self):
        return self.category_name



class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True,related_name="sub_category")
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,null=True,blank=True)
    is_publish = models.BooleanField(default=True)
    no_of_slot = models.IntegerField()
    subcategory_image = models.ImageField(upload_to='sub_category_images')
    

    # @property
    # def all_images(self):
    #     return self.subcategory_images.all()

    def save(self,*arg,**kwargs):
        self.slug = slugify(self.category_name)
        super(SubCategory, self).save(*arg,**kwargs)

    def __str__(self):
        return self.category_name


class TimeSlot(BaseModel):
    service = models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="time_slot")
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['start_time']


class Service(BaseModel):
    service_name = models.CharField(max_length=100)
    is_publish = models.BooleanField(default=True)
    slug = models.SlugField(unique=True,null=True,blank=True)

    def save(self,*arg,**kwargs):
        self.slug = slugify(self.service_name)
        super(Service, self).save(*arg,**kwargs)

    def __str__(self):
        return self.service_name
        

class Product(BaseModel):
    product_name = models.CharField(max_length=200)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True,blank=True,related_name="products")
    mrp_price = models.IntegerField()
    dis_price = models.IntegerField()
    product_description = RichTextField()
    is_publish = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True,null=True,blank=True)
    fake_review = models.IntegerField(null=True,blank=True)
    fake_rating = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    image = models.ImageField(upload_to='images')

    def save(self,*arg,**kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*arg,**kwargs)

    def __str__(self):
        return self.product_name

    def total_reviews(self):
        return self.product_reviews.all().count()
        
    @property
    def average_rating(self):
        return self.product_reviews.aggregate(Avg('rating'))['rating__avg']

    @property
    def total_bookings(self):
        # Calculate the total number of bookings for this product
        return self.booking_set.count()


class ServiceProduct(BaseModel):
    service = models.ForeignKey(Service, on_delete=models.CASCADE,null=True,blank=True,related_name="servicetype")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.service.service_name

    
    
class SubCategoryImage(BaseModel):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,related_name="subcategory_images")
    image = models.ImageField(upload_to="subcategory")

    def __str__(self):
        return self.subcategory.category_name


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimun_amount = models.IntegerField(default=500)


class CityService(BaseModel):
    city_name = models.CharField(max_length = 180,unique=True)
    category  = models.ManyToManyField(Category,related_name="city_service")

    def __str__(self):
        return self.city_name



