from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from product.models import Product,Coupon ,Category,SubCategory,TimeSlot
from django.core.validators import MaxValueValidator, MinValueValidator
from base.models import BaseModel
from django.utils.timezone import now
import uuid
# Create your models here.

class User(AbstractUser):
    username = None
    first_name = None
    last_name= None
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=12,unique=True)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=True)
    otp_time = models.DateTimeField(blank=True,null=True)
    expo_token = models.TextField()
    is_subadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['full_name']
    objects = UserManager()


class StaffWorkType(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="staff_work_type")
    sub_category = models.ForeignKey(SubCategory,on_delete=models.CASCADE)


class SubAdminServiceArea(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="subadmin_service_area")
    city_name = models.CharField(max_length = 180)


class Address(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="address")
    name = models.CharField(max_length=200)
    addressline = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=200)


STATUS_CHOICES = (
    ('Pending','Pending'),
    ('Accepted','Accepted'),
    ('On The Way','On The Way'),
    ('Completed','Completed'),
    ('Canceled','Canceled')
)

 
class Subscribe(BaseModel):
    email = models.EmailField()


class ProductReview(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True,blank=True,related_name="product_reviews")
    rating = models.SmallIntegerField( default=0,validators=[MaxValueValidator(5),MinValueValidator(1)])
    comment = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class Booking(BaseModel):
    invoice_no = models.CharField(max_length=40)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assign_work = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="assign_work",null=True,blank=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.SET_NULL ,null=True,blank=True)
    booking_time = models.DateField()  
    merchantTransactionId = models.CharField(max_length=200)
    transactionId = models.CharField(max_length=200)
    paid_amount = models.CharField(max_length=200)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    staff_status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    name = models.CharField(max_length=200)
    addressline = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    email = models.EmailField(max_length=200)

    otp = models.CharField(max_length=6,null=True)
    otp_time = models.DateTimeField(blank=True,null=True)
    is_otp_verified = models.BooleanField(default=False)

    notes = models.TextField()

    class Meta:
        unique_together = ('time_slot', 'booking_time','assign_work',)
        ordering = ['-created_at']

    @property
    def all_staff(self):
        return User.objects.filter(is_staff=True).filter(address__city=self.city).filter(staff_work_type__sub_category=self.time_slot.service).distinct()

    
    def save(self, *args, **kwargs):
        if not self.invoice_no:
            self.invoice_no = self.generate_invoice_no()
        super().save(*args, **kwargs)

    def generate_invoice_no(self):
        # Generate a unique invoice number
        date_str = now().strftime('%Y%m%d')
        unique_id = uuid.uuid4().hex[:6].upper()
        return f'CA{date_str}{unique_id}'


BOOKING_CHOICES = (
    ('Pending','Pending'),
    ('Accepted','Accepted'),
    ('Hold','Hold'),
    ('Changed','Changed'),
    ('Completed','Completed'),
    ('Canceled','Canceled')
)



class BookingProduct(BaseModel):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name="booking_prod_det")
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,blank=True,related_name="booking_product")
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    staff_work_status = models.CharField(max_length=50,null=True,blank=True)


class BookingHistory(BaseModel):
    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name="booking_history")
    staff_status = models.CharField(max_length=50,choices=BOOKING_CHOICES,default='Pending')
    assignto = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_to')
    assignby = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_by')
    class Meta:
        ordering = ['-created_at']


class RejectReason(BaseModel):
    title = models.TextField()
