from django.shortcuts import render,redirect
from product.models import *
from account.models import *
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth import login,logout,authenticate
from account.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta,datetime
from django.db import IntegrityError
from .helpers import convet_date,get_geo_location
from django.contrib.auth.decorators import login_required

from decouple import config
from django.core.serializers.json import DjangoJSONEncoder
from threading import Timer
import requests
import base64
import json
import hashlib
import random
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from . models import Estimate,Contact,NewAccount

# Create your views here.

def home(request):
    if request.method =="POST":
        name = request.POST['name']
        email = request.POST['email']
        city_name = request.POST['city_name']
        service = request.POST['service']
        message = request.POST['message']
        estimate = Estimate(
            name=name,email=email,city_name=city_name,service=service,
            message=message
        )
        estimate.save()
     
    address = request.GET.get('address')
    query = request.GET.get('query')
    lg = request.GET.get('lg')
    lt = request.GET.get('lt')
    
    if address:
        request.session["address"] = address
        category = Category.objects.filter(is_publish=True).filter(city_service__city_name__iexact=address)
        print("category",category)
        service = Service.objects.filter(is_publish=True).filter(servicetype__category__city_service__city_name__iexact=address).distinct()
        most_booked_services = Product.objects.filter(is_publish=True).filter(booking_set__city__iexact = address).annotate(num_bookings=Count('booking_set')).order_by('-num_bookings')[:10]
        if query:
            product = Product.objects.filter(is_publish=True).filter(sub_category__category__city_service__city_name__iexact=address).filter(product_name__icontains=query)
            context ={'category':category,"product":product}
            return render(request,'search.html',context)
    elif lg and lt:
        address = get_geo_location(lg,lt)
        print(address)
        request.session["address"] = address
        category = Category.objects.filter(is_publish=True).filter(city_service__city_name__iexact=address)
        print("category",category)
        service = Service.objects.filter(is_publish=True).filter(servicetype__category__city_service__city_name__iexact=address).distinct()
        most_booked_services = Product.objects.filter(is_publish=True).filter(booking_set__city__iexact = address).annotate(num_bookings=Count('booking_set')).order_by('-num_bookings')[:10]
        if query:
            product = Product.objects.filter(is_publish=True).filter(sub_category__category__city_service__city_name__iexact=address).filter(product_name__icontains=query)
            context ={'category':category,"product":product}
            return render(request,'search.html',context)
    elif request.session.get('address'):
        address = request.session.get('address')
        print(address)
        category = Category.objects.filter(is_publish=True).filter(city_service__city_name__iexact=address)
        print("category",category)
        service = Service.objects.filter(is_publish=True).filter(servicetype__category__city_service__city_name__iexact=address).distinct()
        # most_booked_services = Product.objects.filter(is_publish=True).filter(booking_set__city__iexact = address).annotate(num_bookings=Count('booking_set')).order_by('-num_bookings')[:10]
        most_booked_services = Product.objects.filter(is_publish=True)
        if query:
            product = Product.objects.filter(is_publish=True).filter(sub_category__category__city_service__city_name__iexact=address).filter(product_name__icontains=query)
            context ={'category':category,"product":product}
            return render(request,'search.html',context)
    else:      
        category = Category.objects.filter(is_publish=True)
        service = Service.objects.filter(is_publish=True)
        most_booked_services = {}

    print(most_booked_services)
    city_services  = CityService.objects.values_list('city_name', flat=True)
    city_service = list(city_services)
    context = {'category':category,'service':service,'most_booked_services':most_booked_services,'city_service':city_service,'address':address}
    return render(request,'index.html',context)


def ulogout(request):
    logout(request)
    return redirect('/')


def service(request,slug):
    subcategory = SubCategory.objects.get(slug=slug)
    allsubcategory= SubCategory.objects.filter(category__uid=subcategory.category.uid).filter(is_publish=True)
    context = {'subcategory':subcategory,'allsubcategory':allsubcategory}
    return render(request,'service.html',context)


def cart(request):
    return render(request,'cart.html')


def add_to_cart(request):
    uid = request.GET.get('uid')
    quantity = request.GET.get('quantity')
    product = Product.objects.get(uid=uid)
    # if product.sub_category == 
    cart = request.session.get('cart')  
    if cart:
        psubcategory = Product.objects.get(uid=list(cart)[0])
        if product.sub_category == psubcategory.sub_category:
            print("hai")
            desc = cart.get(uid)
            if desc:
                print('product in cart')
                cart[uid] = quantity
            else:
                print('product not in cart')
                cart[uid] = quantity
        else:
            print('nahi h')
            del request.session['cart']
            cart ={}  
            cart[uid]=quantity
    else:
        cart ={}  
        cart[uid]=quantity
    request.session['cart']=cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def deletesessioncart(request,uid):
    cart = request.session['cart']
    del cart[str(uid)]
    request.session["cart"] = cart
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="userlogin")
def checkout(request):
    if request.method == "POST":        
        booking_date = request.POST['booking_date']
        print(booking_date)
        time_slot = request.POST["time_slot"]
        if booking_date == "" and time_slot =="":
            messages.error(request, "Please check Date and time slot")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if time_slot =="":
            messages.error(request, "Please check Date and time slot")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        name = request.POST['full_name']
        saddress = request.POST['address']
        locality = request.POST['locality']
        city = request.POST['city']
        zipcode = request.POST['zipcode']
        state = request.POST['state']
        phone = request.POST['mobile']
        email = request.POST['email']
        cod = request.POST.get('cod')
        try:
            address=Address(user=request.user,name=name,addressline=saddress,locality=locality,city=city,zipcode=zipcode,
                                 state=state,phone=phone,email=email)
            address.save()
        except IntegrityError as e:
            address= Address.objects.get(user=request.user)
            address.name = name
            address.addressline = saddress
            address.locality = locality
            address.city = city
            address.zipcode = zipcode
            address.state = state
            address.phone= phone
            address.email =email
            address.save()
        cart = request.session.get('cart') 
        product = []
        totalamount = 0
        if cart:
            for k in cart:
                queryset =Product.objects.get(uid=k)
                queryset.quantity = cart[k]
                if queryset.quantity:
                    totalamount = totalamount + (queryset.dis_price*int(queryset.quantity))
                else:
                    pass
                product.append(queryset) 
        print(totalamount)
        if cod:
            booking = Booking(
                user = request.user,
                time_slot = TimeSlot.objects.get(uid=time_slot),
                booking_time = booking_date,
                name=name,addressline=saddress,locality=locality,city=city,zipcode=zipcode,
                state=state,phone=phone,email=email,
                paid_amount = totalamount,
                transactionId = "cod",
                merchantTransactionId="cod"
            )
            booking.save()
            for p in product:
                bookingproduct = BookingProduct(
                        booking= booking,
                        product=p,
                        quantity=p.quantity
                    )
                bookingproduct.save()           
            del request.session['cart']
            return redirect('thankyou')
        else:
            data = {
                "merchantId":config('MERCHANT_ID'),
                "merchantTransactionId": 'MT'+ phone + str(random.randint(10000, 99999)),
                "merchantUserId":'MU'+ phone,
                "amount": totalamount*100,
                "redirectUrl": "https://casaxprt.com/thankyou",
                "redirectMode": "POST",
                "callbackUrl": "https://casaxprt.com/paymentcallback",
                "mobileNumber": phone,
                "paymentInstrument": {
                "type": "PAY_PAGE"
                }
                }
            print(data)
            json_data = json.dumps(data)
            encoded_dict = json_data.encode('utf-8')
            encoded_data =base64.b64encode(encoded_dict)
            string = base64.b64encode(encoded_dict) + ("/pg/v1/pay" ).encode('utf-8') +(config('SALT_KEY')).encode('utf-8') 
            url = f"{config('PAYMENT_URL')}/pg/v1/pay"
            print(encoded_data.decode('utf-8'))
            payload = {"request":encoded_data.decode('utf-8')}
            sha_con =hashlib.sha256(string).hexdigest()
            xverify = (sha_con)+ '###' +'1'
            print(xverify)
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "X-VERIFY":xverify
            }
            response = requests.post(url,json=payload, headers=headers,)
            print(response)
            response =response.json()
            print(response)
            if response['success']== False:
                return HttpResponse('payment faild')
            paymenturl =response['data']['instrumentResponse']['redirectInfo']['url']
            merchantTransactionId = response['data']['merchantTransactionId']  
            booking = Booking(
                user = request.user,
                # product = product,
                quantity = qty,
                time_slot = TimeSlot.objects.get(uid=time_slot),
                booking_time = booking_date,
                name=name,addressline=saddress,locality=locality,city=city,zipcode=zipcode,
                state=state,phone=phone,email=email,
                paid_amount = totalamount,    
                merchantTransactionId=merchantTransactionId,
                is_paid=False,
                )
            booking.save()
            for p in product:
                bookingproduct = BookingProduct(
                        booking= booking,
                        product=p,
                        quantity=p.quantity
                    )
                bookingproduct.save()          
            del request.session['cart']
            print(booking)
            return redirect(paymenturl)
    sdate = request.GET.get('sdate')   
    cart = request.session.get('cart')  
    if cart:
        product = Product.objects.get(uid=list(cart)[0])
        sub_cat = product.sub_category
    else:
        return redirect('cart')
    if sdate:
        act_date = convet_date(sdate)
    else:
        current_date = datetime.now()
        act_date = current_date.strftime("%Y-%m-%d") 
    current_date = datetime.now().date()
    next_four_days = [
        {
            'date': current_date + timedelta(days=i),
            'is_active': str(current_date + timedelta(days=i)) == str(act_date)
        }
        for i in range(4)
    ]
    time_slot = TimeSlot.objects.filter(service=sub_cat)
    for t in time_slot:
        get_booking = Booking.objects.filter(time_slot__service=sub_cat).filter(booking_time =act_date).filter(time_slot=t).count()
        if get_booking < sub_cat.no_of_slot:
            t.availble=True
        else:
            t.availble=False
    context = {"time_slot":time_slot,'next_four_days':next_four_days,'act_date':act_date}
    return  render(request,'checkout.html',context)


@csrf_exempt
def check_status(merchantTransactionIds):
    print('functions called')
    url = f"{config('PAYMENT_URL')}/pg/v1/status/{config('MERCHANT_ID')}/{merchantTransactionIds}"
    string = f"/pg/v1/status/{config('MERCHANT_ID')}/{merchantTransactionIds}{config('SALT_KEY')}"
    enc = string.encode('utf-8')
    sha_con =hashlib.sha256(enc).hexdigest()
    xverify = (sha_con)+ '###' +'1'
    print(xverify)
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "X-VERIFY": xverify,
        "X-MERCHANT-ID": config('MERCHANT_ID')
    }
    response = requests.get(url, headers=headers)
    response =response.json()
    mydata =response['data']
    if mydata['code'] == "PAYMENT_SUCCESS":
        print("payment succes")     
        try:
            book = OrderPlaced.objects.get(merchantTransactionId=mydata['data']['merchantTransactionId'],is_paid=False)
        except book.DoesNotExist:
            pass
        total_cart = OrderPlaced.objects.filter(is_paid=True).count()
        # if cart.coupon:
        #     coupon = Coupon.objects.get(coupon_code=cart.coupon.coupon_code)
        #     coupon.is_expired = True
        #     coupon.save()
        invoice = '0000' + str(total_book + 1)
        lent = len(invoice)
        invoice_nos = "ORN" + invoice[lent-4:]
        book.invoice_no = invoice_nos
        book.transactionId = transactionIds
        book.paid_amount = int(mydata['data']['amount'])/100
        book.ordered_date = datetime.now()
        book.is_paid = True 
        book.save() 

        cart = request.session['cart']
        del cart[str(book.product.uid)]
        request.session["cart"] = cart
        return HttpResponse("payment success")


@csrf_exempt
def paymentcallback(request):
    received_json_data=json.loads(request.body)
    decoded_data = base64.b64decode(received_json_data['response'])
    print(decoded_data)
    mydata = json.loads(decoded_data)
    print(mydata['success'])
    merchantTransactionIds = mydata['data']['merchantTransactionId']
    transactionIds = mydata['data']['transactionId']
    if mydata['code'] == "PAYMENT_SUCCESS":
        print("payment succes")     
        try:
            book = Booking.objects.get(merchantTransactionId=merchantTransactionIds,is_paid=False)
        except book.DoesNotExist:
            pass
        total_book = Booking.objects.filter(is_paid=True).count()
        # if book.coupon:
        #     coupon = Coupon.objects.get(coupon_code=book.coupon.coupon_code)
        #     coupon.is_expired = True
        #     coupon.save()
        invoice = '0000' + str(total_book + 1)
        lent = len(invoice)
        invoice_nos = "ORN" + invoice[lent-4:]
        book.invoice_no = invoice_nos
        book.transactionId = transactionIds
        book.paid_amount = int(mydata['data']['amount'])/100
        book.ordered_date = datetime.now()
        book.is_paid = True 
        book.save()             
        cart = request.session['cart']
        del cart[str(book.product.uid)]
        request.session["cart"] = cart
        return HttpResponse("payment success")
    elif mydata['code'] == "PAYMENT_PENDING":
        t = Timer(25.0, check_status,[merchantTransactionIds])
        t.start()
    else:
        return HttpResponse("payment Fail")


@csrf_exempt
def thankyou(request):
    return render(request,'thankyou.html')


def address(request):
    if request.method == "POST":
        name = request.POST['full_name']
        saddress = request.POST['address']
        locality = request.POST['locality']
        city = request.POST['city']
        zipcode = request.POST['zipcode']
        state = request.POST['state']
        phone = request.POST['mobile']
        email = request.POST['email']
        try:
            address=Address(user=request.user,name=name,addressline=saddress,locality=locality,city=city,zipcode=zipcode,
                                 state=state,phone=phone,email=email)
            address.save()
        except IntegrityError as e:
            address= Address.objects.get(user=request.user)
            address.name = name
            address.addressline = saddress
            address.locality = locality
            address.city = city
            address.zipcode = zipcode
            address.state = state
            address.phone= phone
            address.email =email
            address.save()
    return render(request,'profile/address.html')


def help(request):
    return render(request,'profile/help.html')


def order(request):
    uid = request.GET.get('uid')
    if uid:
        booking = Booking.objects.get(uid = uid)
        booking_timeslot = timezone.make_aware(datetime.combine(booking.booking_time,booking.time_slot.start_time))
        time_diff = booking_timeslot- timezone.localtime(timezone.now())
        print(time_diff)
        print(timezone.localtime(timezone.now()))
        delta = timedelta(hours=1, minutes=00, seconds=0)
        print(time_diff <= delta)
        if time_diff <= delta:
            messages.error(request,'Cancelation time expired') 
            return redirect('order')    
        booking.status = 'Canceled'
        booking.staff_status = 'Canceled'
        booking.save()
        messages.success(request,"Order cancelled successfully")

    booking = Booking.objects.filter(user=request.user)
    context = {'booking':booking}
    return render(request,'profile/order.html',context)


def profile(request):
    if request.method =="POST":
        name = request.POST['name']
        email = request.POST['email']
        user = request.user
        user.full_name = name
        user.email = email
        user.save()
    return render(request,'profile/profile.html')
    

def register_as_a_professional(request):
    if request.method =="POST":
        phone = request.POST['phone']
        
        newaccount = NewAccount.objects.filter(phone=phone).first()
        if newaccount:
            pass
        else:
            newaccount = NewAccount(
                phone=phone
            )
            newaccount.save()
    return render(request,'regisAsAProfessional.html')


def gallery(request):
    return render(request,'gallery.html')


def contact(request):
    if request.method =='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        subject = request.POST['subject']
        message = request.POST['message']
        contact = Contact(name=name,email=email,phone=phone,subject=subject,message=message)
        contact.save()
        messages.success(request,"you message is sended successfully")
    return render(request,'contact.html')


@csrf_exempt
def verifyotp(request):
    if request.method == "POST":
        phone_number = request.POST['phone_number']
        otp = request.POST.get('otp')
        try:
            user_obj = User.objects.get(phone_number=phone_number)
        except Exception as e:
            messages.error(request, "Please check Mobile no")
            context = {'phone_number':phone_number}
            return render(request, 'otpverify.html',context)
        if user_obj.otp == otp:
            time_diff = timezone.now() - user_obj.otp_time
            delta = timedelta(hours=0, minutes=10, seconds=0)
            if time_diff >= delta:
                messages.error(request, "Otp expired")
                return HttpResponseRedirect(request.path_info)  
            login(request, user_obj)  
            return redirect('/')  
        else:
            messages.error(request, "Invalid OTP")
            return HttpResponseRedirect(request.path_info)              
    context = {'mobile':mobile}
    return redirect('/')



def userlogout(request):
    logout(request)
    return redirect('/')


def about(request):
    return render(request,'about.html')


def faq(request):
    return render(request,'faq.html')


def privacy_policy(request):
    return render(request,'privacy-policy.html')


def terms_and_conds(request):
    return render(request,'terms-and-conditions.html')


def error_404_view(request, exception):
    return render(request, '404.html')