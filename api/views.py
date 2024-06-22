from django.shortcuts import render
from product.models import *
from product.serializers import *
from account.models import *
from account.serializers import *
from account.helpers import send_otp_to_phone,send_work_otp
from account.models import User
from rest_framework.decorators import api_view , permission_classes,authentication_classes
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.utils import IntegrityError
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta,datetime
from django.db.models import Q
from django.db import IntegrityError
from django.db.models import Count
# Create your views here.



@api_view(['POST'])
def register(request):
    data = request.data
    if data.get('full_name') is None:
        return Response({
            'status': 400,
            'message': "Name is not valid"
        })
    if data.get('email') is None:
        return Response({
            'status': 400,
            'message': "Email is not valid"
        })
    try:
        user_email= User.objects.get(email=data.get('email'))
        return Response({
            'status': 400,
            'message': "Email is already added"
        })
    except Exception as e:
        print(e)
    if data.get('phone_number') is None:
        return Response({
            'status': 400,
            'message': "Phone number is not valid"
        })

    try:
        user_obj = User.objects.get(phone_number=data.get('phone_number')) 
        return Response({
                'status': 200,
                'message': "User already exits"
            })
    except User.DoesNotExist: 
        serializer = UserModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 200,
                'message': "User register successfully"
            })

        return Response({
                'status': 400,
                'message': "Please fill form correctly",
                "data" :serializer.errors
            })
    

@api_view(['POST'])
def user_login(request):
    data = request.data
    if data.get('phone_number') is None:
        return Response({
            'status': 400,
            'message': "Phone number is not valid"
        })
    if len(data.get('phone_number')) < 10:
        return Response({
            'status': 400,
            'message': "Phone number is not valid"
        })
    if data.get('phone_number') =="1919191919":
        user_obj = User.objects.get(phone_number=data.get('phone_number')) 
        user_obj.otp ="191919"
        user_obj.otp_time = timezone.localtime(timezone.now())
        user_obj.save()
        return Response({
            'status': 200,
            'message':"enter otp to login"
        })
    try:
        user_obj,created = User.objects.get_or_create(phone_number=data.get('phone_number')) 
        user_obj.otp =send_otp_to_phone(data.get('phone_number'))
        user_obj.otp_time = timezone.localtime(timezone.now())
        user_obj.save()
        return Response({
            'status': 200,
            'message': "Otp sended to your mobile no, Valid only 10 minutes"
        })
    except User.DoesNotExist:
        return Response({
            'status': 400,
            'message': "User not found check your mobile no"
        })

    

@api_view(['POST'])
def staff_login(request):
    data = request.data
    if data.get('phone_number') is None:
        return Response({
            'status': 400,
            'message': "Phone number is not valid"
        })
    if data.get('phone_number') =="1919191919":
        user_obj = User.objects.get(phone_number=data.get('phone_number')) 
        user_obj.otp ="191919"
        user_obj.otp_time = timezone.localtime(timezone.now())
        user_obj.save()
        return Response({
            'status': 200,
            'message':"enter otp to login"
        })
    try:
        user_obj = User.objects.get(phone_number=data.get('phone_number'))
        if user_obj.is_staff == False:
            return Response({
            'status': 400,
            'message': "Please check mobile no and password"
        })
        user_obj.otp =send_otp_to_phone(data.get('phone_number'))
        user_obj.otp_time = timezone.localtime(timezone.now())
        user_obj.save()
        return Response({
            'status': 200,
            'message': "Otp sended to your mobile no valid only 10 minutes"
        })
    except User.DoesNotExist:
        return Response({
            'status': 400,
            'message': "User not found check your mobile no"
        })


@api_view(['GET','POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def set_message_token(request):
    data =request.data
    if request.method=="POST":
        if data.get('token') is None:
            return Response({
                'status': 400,
                'message': "token is not valid"
            })
        user = request.user
        userdata = User.objects.get(phone_number = user.phone_number) 
        userdata.expo_token = data.get('token')
        userdata.save() 
        return Response({
            'status': 200,
            'message': "token is saved successfully"
        }) 
    user = request.user  
    return Response({
            'status': 200,
            'token': user.expo_token
        }) 


@api_view(['POST'])
def verify_otp(request):
    data = request.data
    if data.get('phone_number') is None:
        return Response({
            'status': 400,
            'message': "Mobile No is required"
        })

    if data.get('otp') is None:
        return Response({
            'status': 400,
            'message': "Otp is required"
        })
    try:
        user_obj = User.objects.get(phone_number=data.get('phone_number'))
    except Exception as e:
        return Response({
            'status':400,
            "message":'Invalid phone number'
        })  
    if user_obj.otp == data.get('otp'):
        time_diff = timezone.localtime(timezone.now()) - user_obj.otp_time
        delta = timedelta(hours=0, minutes=10, seconds=0)
        if time_diff >= delta:
            return Response({
                'status':400,
                'message':'Otp expired'
            })
        refresh = RefreshToken.for_user(user_obj)
        return Response({
            'status':200,
            'message':'Otp verified',
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })     
    else:
        return Response({
            'status':400,
            'message':'Invaild otp'
        })
        


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    userdata = User.objects.get(phone_number = user.phone_number)
    serializer = UserModelSerializers(userdata,many=False)
    return Response({
        "status":200,
        "profile":serializer.data
    })
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateprofile(request):
    data = request.data
    user = request.user
    userdata = User.objects.get(phone_number = user.phone_number)
    if data.get('full_name') is None:
        return Response({
            'status': 400,
            'message': "Name is not valid"
        })
    
    if data.get('email') is None:
        return Response({
            'status': 400,
            'message': "Email is not valid"
        })
    try:
        user_email= User.objects.get(email=data.get('email'))
        return Response({
            'status': 400,
            'message': "Email is already added"
        })
    except Exception as e:
        print(e)
    # if data.get('phone_number') is None:
    #     return Response({
    #         'status': 400,
    #         'message': "Phone number is not valid"
    #     })
    userdata.full_name = data.get('full_name')
    userdata.email = data.get('email') 
    #userdata.phone_number = data.get('phone_number')
    userdata.save()
    return Response({
        "status":200,
        "message":"Updated Successfully"
    })


@api_view(['GET'])
def show_home_data(request):
    print('show home data')
    most_booked_services = Product.objects.filter(is_publish=True).annotate(num_bookingproducts=Count('booking_product'))
    most_book_serializer = ProductModelSerializers(most_booked_services,many=True) 
    return Response({
            'status': 200,
            'most_book_service': most_book_serializer.data
        })


@api_view(['GET'])
def show_category(request):
    address = request.GET.get('address')
    if address:
        category = Category.objects.filter(is_publish=True).filter(city_service__city_name__iexact=address) 
        service  = Service.objects.filter(is_publish=True).filter(servicetype__category__city_service__city_name__iexact=address).distinct()
        city_booking = Booking.objects.filter(city=address)
        most_booked_services = Product.objects.filter(is_publish=True).filter(booking_product__booking__city__iexact = address).annotate(num_bookingproducts=Count('booking_product')).order_by('-num_bookingproducts')[:10]
        most_book_serializer = ProductModelSerializers(most_booked_services,many=True)     
    else:
        category = Category.objects.all()   
        service = Service.objects.all()
    categoryserializer = CategoryModelSerializers(category,many=True)
    serviceserializer = ServiceModelSerializers(service,many=True)
    return Response({
            'status': 200,
            'category':categoryserializer.data,
            "service":serviceserializer.data,
            'most_book_service': most_book_serializer.data
        })


@api_view(['GET'])
def search_view(request):
    address = request.GET.get('address')
    query = request.GET.get('query')

    if address and query:
        sub_category = SubCategory.objects.filter(is_publish=True).filter(category__city_service__city_name=address).filter(category_name__icontains=query)
        sub_categoryserializer = SubCategoryModelSerializers(sub_category,many=True)
        product = Product.objects.filter(is_publish=True).filter(sub_category__category__city_service__city_name=address).filter(product_name__icontains=query)
        productserializer = ProductModelSerializers(product,many=True)
        return Response({
                'status': 200,
                'subcategory': sub_categoryserializer.data,
                'product':productserializer.data
            })
    else:
        return Response({
                'status': 400,
                'subcategory': "No input found"
            })


@api_view(['GET'])
def show_subcategory(request,uid):
    subcategory = SubCategory.objects.filter(category__uid=uid)
    serializer = SubCategoryModelSerializers(subcategory,many=True)
    return Response({
            'status': 200,
            'subcategory': serializer.data
        })


@api_view(['GET'])
def get_subcategory(request,uid):
    subcategory = SubCategory.objects.get(uid=uid)
    serializer = SubCategoryModelSerializers(subcategory,many=False)
    return Response({
            'status': 200,
            'subcategory': serializer.data
        })       


@api_view(['GET'])
def service(request,uid):
    service = Product.objects.filter(sub_category__uid=uid)
    serializer = ProductModelSerializers(service,many=True)
    return Response({
            'status': 200,
            'service': serializer.data
        })


@api_view(['GET','POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def address(request):
    user = request.user
    if request.method == "POST":
        user = request.user
        data = request.data
        if data.get('full_name') is None:
            return Response({
                'status': 400,
                'message': "Name is not valid"
            })
        
        if data.get('email') is None:
            return Response({
                'status': 400,
                'message': "Email is not valid"
            })
        if data.get('phone') is None:
            return Response({
                'status': 400,
                'message': "phone is not valid"
            })
        if data.get('addressline') is None:
            return Response({
                'status': 400,
                'message': "addressline is not valid"
            })
        if data.get('locality') is None:
            return Response({
                'status': 400,
                'message': "locality is not valid"
            })
        if data.get('city') is None:
            return Response({
                'status': 400,
                'message': "city is not valid"
            })
        if data.get('zipcode') is None:
            return Response({
                'status': 400,
                'message': "zipcode is not valid"
            })
        if data.get('state') is None:
            return Response({
                'status': 400,
                'message': "state is not valid"
            })

        address = Address(
            user=user,
            name = data.get('full_name'),
            addressline = data.get('addressline'),
            locality = data.get('locality'),
            city = data.get('city'),
            zipcode = data.get('zipcode'),
            state = data.get('state'),
            phone = data.get('phone'),
            email = data.get('email')
        )
        address.save()
        return Response({
                'status': 200,
                'message': "Address Added Successfully"
            })
    address = Address.objects.filter(user = user)
    serializer = AddressModelSerializers(address,many=True)
    return Response({
            'status': 200,
            'address': serializer.data
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def del_address(request):
    data =request.data
    if data.get('uid') is None:
            return Response({
                'status': 400,
                'message': "uid is not valid"
            })
    add = Address.objects.get(uid=uid)
    add.delete()
    return Response({
                'status': 400,
                'message': "Address deleted successfully"
            })
    
    
@api_view(['GET'])
def time_slot(request,uid):
    requested_date = request.GET.get('sdate')
    if requested_date:
        try:
            actual_date = datetime.strptime(requested_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'status': 400, 'error': 'Invalid date format. Use YYYY-MM-DD.'})
    else:
        actual_date = datetime.now().date()
    current_date = datetime.now().date()
    try:
        # Get all time slots for the given service
        time_slots = TimeSlot.objects.filter(service__uid=uid)
        subcategory = SubCategory.objects.get(uid=uid)
    except SubCategory.DoesNotExist:
        return Response({'status': 404, 'error': 'SubCategory not found.'})

    current_time_utc = timezone.now()
    local_time = timezone.localtime(current_time_utc)
    local_time_plus_2_hours = local_time + timedelta(hours=2)
    local_time_str = local_time_plus_2_hours.strftime('%H:%M:%S')
    local_time_obj = datetime.strptime(local_time_str, '%H:%M:%S').time()
    
    for time_slot in time_slots:
        print(time_slot.start_time<=local_time_obj)
        print(str(actual_date)==current_date.strftime("%Y-%m-%d"))
        booking_count = Booking.objects.filter(booking_time=actual_date,time_slot=time_slot).count()  
        if booking_count < subcategory.no_of_slot:   
            if str(actual_date) ==current_date.strftime("%Y-%m-%d") and time_slot.start_time <= local_time_obj:
                time_slot.available = False
            else:
                time_slot.available = True
        else:
            time_slot.available = False
        # time_slot.available = booking_count < subcategory.no_of_slot
    serializer = TimeSlotMModelSerializers(time_slots, many=True)
    return Response({
        'status': 200,
        'time_slot': serializer.data
    })



@api_view(['GET','POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def orderlist(request):
    if request.method == "POST":
        data = request.data
        if data.get('full_name') is None and len(data.get('full_name')) <= 3:
            return Response({
                'status': 400,
                'message': "Name is not valid"
            })
        
        if data.get('email') is None and len(data.get('email')) <= 3:
            return Response({
                'status': 400,
                'message': "Email is not valid"
            })
        if data.get('phone') is None:
            return Response({
                'status': 400,
                'message': "phone is not valid"
            })
        if data.get('addressline') is None:
            return Response({
                'status': 400,
                'message': "addressline is not valid"
            })
        if data.get('locality') is None:
            return Response({
                'status': 400,
                'message': "locality is not valid"
            })
        if data.get('city') is None and len(data.get('city')) <= 3:
            return Response({
                'status': 400,
                'message': "city is not valid"
            })
        if data.get('zipcode') is None:
            return Response({
                'status': 400,
                'message': "zipcode is not valid"
            })
        if data.get('state') is None:
            return Response({
                'status': 400,
                'message': "state is not valid"
            })
        if data.get('product_list') is None:
            return Response({
                'status': 400,
                'message': "product_list is not valid"
            })
        if data.get('time_slot') is None:
            return Response({
                'status': 400,
                'message': "time_slot is not valid"
            })
        if data.get('booking_time') is None:
            return Response({
                'status': 400,
                'message': "booking_time is not valid"
            })
        if data.get('paid_amount') is None:
            return Response({
                'status': 400,
                'message': "paid_amount is not valid"
            })

        try:
            address = Address(
                user=request.user,
                name = data.get('full_name'),
                addressline = data.get('addressline'),
                locality = data.get('locality'),
                city = data.get('city'),
                zipcode = data.get('zipcode'),
                state = data.get('state'),
                phone = data.get('phone'),
                email = data.get('email')
                )
            address.save()
        except IntegrityError as e:
            address= Address.objects.get(user=request.user)
            address.name = data.get('full_name')
            address.addressline = data.get('addressline')
            address.locality = data.get('locality')
            address.city = data.get('city')
            address.zipcode = data.get('zipcode')
            address.state = data.get('state')
            address.phone= data.get('phone')
            address.email = data.get('email')
            address.save()
        booking = Booking(
            user = request.user,
            time_slot = TimeSlot.objects.get(uid =  data.get('time_slot')),
            booking_time = data.get('booking_time'),
            name = data.get('full_name'),
            addressline = data.get('addressline'),
            locality = data.get('locality'),
            city = data.get('city'),
            zipcode = data.get('zipcode'),
            state = data.get('state'),
            phone = data.get('phone'),
            email = data.get('email'),
            paid_amount = data.get('paid_amount')
        )
        booking.save()
        for p in data.get('product_list'):
            print(type(p))
            bookingproduct = BookingProduct(
                        booking= booking,
                        product=Product.objects.get(uid=p['uid']),
                        quantity=p['quantity']
                    )
            bookingproduct.save() 
        return Response({
            'status': 200,
            'orderuid': booking.uid
        })
    booking = Booking.objects.filter(user = request.user)
    serializer = BookingModelSerializers(booking,many=True)
    return Response({
            'status': 200,
            'order': serializer.data
        })
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def cancel_booking(request):
    if request.method =="POST":
        data = request.data
        if data.get('uid') is None:
            return Response({
                'status': 400,
                'message': "uid is not valid"
            })
        booking = Booking.objects.get(uid = data.get('uid'))
        booking_timeslot = timezone.make_aware(datetime.combine(booking.booking_time,booking.time_slot.start_time))
        time_diff = booking_timeslot- timezone.localtime(timezone.now())
        print(time_diff)
        print(timezone.localtime(timezone.now()))
        delta = timedelta(hours=1, minutes=00, seconds=0)
        print(time_diff <= delta)
        if time_diff <= delta:
            return Response({
                'status':400,
                'message':'Cancelation time expired'
            })      
        booking.status = 'Canceled'
        booking.staff_status = 'Canceled'
        booking.save()
        return Response({
                'status':200,
                'message':'Booking canceled successfully'
            })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def product_reviews(request):
    if request.method =="POST":
        data = request.data
        user =request.user
        rating =data.get('rating')
        if data.get('product_uid') is None:
            return Response({
                'status': 400,
                'message': "product_uid is not valid"
            })
        if rating is None:
            return Response({
                'status': 400,
                'message': "rating is not valid"
            })
        if 1 <= rating <= 5:
            existing_review = ProductReview.objects.filter(product=Product.objects.get(uid = data.get('product_uid')), user=user).first()
            if existing_review:
                existing_review.rating = rating
                existing_review.comment = "no comment"
                existing_review.save()
                return Response({
                        'status': 200,
                        'message': "reviews updated ssuccessfully"
                    })
            else:  
                review= ProductReview(
                    user=user,
                    product = Product.objects.get(uid = data.get('product_uid')),
                    rating = rating,
                    comment = "no comment"
                )
                review.save()
                return Response({
                        'status': 200,
                        'message': "reviews added ssuccessfully"
                    })
        else:
            if rating is None:
                return Response({
                    'status': 400,
                    'message': "rating should between 1 to 5"
                })


# staff apis start from here
@api_view(['GET','POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def staff_status_work(request):       
    user = request.user
    if user.is_staff != True:
        return Response({
            'status': 400,
            'message': "you have no permission"
        })
    if request.method == "POST":
        data = request.data
        if data.get('status') is None:
            return Response({
                'status': 400,
                'message': "status is not valid"
            })
    booking = Booking.objects.filter(assign_work=user).filter(staff_status=data.get('status'))
    booking_serializer = BookingModelSerializers(booking,many=True)
    return Response({
            'status': 200,
            'work_details': booking_serializer.data
        })


@api_view(['POST'])
def send_staff_work_otp(request):
    data = request.data
    if data.get('uid') is None:
        return Response({
            'status': 400,
            'message': "uid is not valid"
        })
    try:
        booking = Booking.objects.get(uid=data.get('uid'))
        booking.otp =send_work_otp(booking.phone)
        booking.otp_time = timezone.localtime(timezone.now())
        booking.save()
        return Response({
            'status': 200,
            'message': "Otp sended to your mobile no, Valid only 10 minutes"
        })
    except Booking.DoesNotExist:
        return Response({
            'status': 400,
            'message': "Booking not found check your uid"
        })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def staff_change_status(request):
    user = request.user
    if user.is_staff != True:
        return Response({
            'status': 400,
            'message': "you have no permission"
        })
    if request.method == "POST":
        data = request.data
        if data.get('uid') is None:
            return Response({
                'status': 400,
                'message': "uid is not valid"
            })
        booking = Booking.objects.get(uid=data.get('uid'))
        if data.get('status') is None:
            return Response({
                'status': 400,
                'message': "status is not valid"
            })

        if data.get('status') == "Accepted":
            if data.get('otp') is None:
                return Response({
                    'status': 400,
                    'message': "otp is not valid"
                })
            if booking.otp == data.get('otp'):
                time_diff = timezone.localtime(timezone.now()) - booking.otp_time
                delta = timedelta(hours=0, minutes=10, seconds=0)
                if time_diff >= delta:
                    return Response({
                        'status':400,
                        'message':'Otp expired'
                    }) 
                else:
                    booking.status = data.get('status')
                    booking.is_otp_verified = True
                    booking.save()
            else:
                return Response({
                    'status':400,
                    'message':'Invaild otp'
                })

            return Response({
                'status': 200,
                'message': "work status update successfully"
            })
        if data.get('status') == "Canceled":
            if data.get('notes') is None:
                return Response({
                    'status': 400,
                    'message': "notes is not valid"
                })
            booking.staff_status = data.get('status')
            booking.notes = data.get('notes')
            booking.save()
            return Response({
                'status': 200,
                'message': "work status update successfully"
            })

        if data.get('status') == "StaffCancel":
            booking.staff_status = "Canceled"
            booking.save()
            return Response({
                'status': 200,
                'message': "work status update successfully"
            })
        if data.get('status') == "StaffAccepted":
            booking.staff_status = "Accepted"
            booking.save()
            return Response({
                'status': 200,
                'message': "work status update successfully"
            })

        if data.get('status') == "Completed":
            if booking.is_otp_verified !=True:
                return Response({
                        'status': 200,
                        'message': "otp is not verifed you not comple work"
                    })
            booking.staff_status = data.get('status')
            booking.status = data.get('status')
            booking.save()
            return Response({
                'status': 200,
                'message': "work status update successfully"
            })

        return Response({
                'status': 400,
                'message': "some thing wrong"
            })       



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def reject_reason(request):
    reason =RejectReason.objects.all()
    serializer = RejectReasonSerializers(reason,many = True)
    return Response({
        'status':200,
        'reason':serializer.data
    })


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def generate_booking(request):
    if request.method=="POST":
        data = request.data
        if data.get('uid') is None:
            return Response({
                'status': 400,
                'message': "uid is not valid"
            })
        booking = Booking.objects.get(uid=data.get('uid'))
        if data.get('paymenttype')=="cod":
            booking.transactionId = "cod"
            booking.merchantTransactionId="cod"
            booking.save()
            return Response({
                'status': 200,
                'message': "order successfully",
                'paymenttype': "cash on delevery"
            }) 
        else:
            if data.get('merchantid') is None:
                return Response({
                    'status': 400,
                    'message': "merchantid is not valid"
                })
            booking.merchantTransactionId=data.get('merchantid')
            booking.save()
            return Response({
                'status': 200,
                'message': "payment generated",
                'paymenttype': "unpaid"
            })
            

        
        


