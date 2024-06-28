from django.shortcuts import render,redirect
from product.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from . models import *
from home.models import Estimate,Contact,NewAccount
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from . form import CityServiceModelForm
from .sendnotification import send_push_notification
from django.db import transaction, IntegrityError
from django.contrib.auth.hashers import make_password
from django.db.models import OuterRef, Subquery

from django.utils import timezone
from datetime import timedelta,datetime

from home.helpers import convet_date,get_geo_location
# Create your views here.

def adminlogin(request):
    if request.user.is_superuser == True:
        return redirect('dashboard')
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        user_obj = User.objects.filter(phone_number=mobile)
        if not user_obj.exists():
            messages.error(request, "Account not found/exits")
            return HttpResponseRedirect(request.path_info)
        user_obj = authenticate(phone_number=mobile,password=password)
        if user_obj:
            login(request, user_obj)
            messages.success(request, "login successfully")
            if user_obj.is_superuser == True or user_obj.is_subadmin==True:
                return redirect('dashboard')
            return redirect('/')
        messages.error(request, "Invalid Creadationls")
        return HttpResponseRedirect(request.path_info)
    return render(request,'adminpannel/adminlogin.html')


@login_required(login_url="adminlogin")
def dashboard(request):
    if (request.user.is_superuser == True) or (request.user.is_subadmin == True):
        pass
    else:
        return redirect('/')
    user_obj =request.user
    # if user_obj.is_staff != True:
    #             return redirect('adminlogin')
    pending_count = Booking.objects.filter(status='Pending',staff_status='Pending',is_paid=True).count()
    assign_work_count = Booking.objects.filter(status='Pending',staff_status='Pending',is_paid=True).count()
    staff_accepted_count = Booking.objects.filter(status='Pending',staff_status='Accepted',is_paid=True).count()
    staff_canceled_count = Booking.objects.filter(status='Pending',staff_status='Canceled',is_paid=True).count()
    completed_count = Booking.objects.filter(status='Completed',staff_status='Canceled',is_paid=True).count()
    cancel_count = Booking.objects.filter(status='Canceled',is_paid=True).count()

    category_count = Category.objects.all().count()
    sub_category_count = SubCategory.objects.all().count()
    products_count = Product.objects.all().count()
    cityservice_count = CityService.objects.all().count()
    context ={
        'pending_count':pending_count,'assign_work_count':assign_work_count,
        'staff_accepted_count':staff_accepted_count,'staff_canceled_count':staff_canceled_count,
        'completed_count':completed_count,'cancel_count':cancel_count,
        'category_count':category_count,'sub_category_count':sub_category_count,
        'products_count':products_count,'cityservice_count':cityservice_count
    }
    return render(request,'adminpannel/index.html',context)


@login_required(login_url="adminlogin")
def addcategory(request):
    user_obj =request.user
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method == "POST":
        title = request.POST['title']
        image = request.FILES['images']
        category = Category(category_name=title,category_image=image)
        category.save()
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'adminpannel/pages/addcategory.html',context)



@login_required(login_url="adminlogin")
def delcategory(request,uid):
    user_obj =request.user
    if request.user.is_superuser != True:
        return redirect('/')
    category = Category.objects.get(uid=uid)
    category.delete()
    return redirect('addcategory')


@login_required(login_url="adminlogin")
def addsubcategory(request):
    user_obj =request.user
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method=="POST":
        title = request.POST['title']
        subcat = request.POST['subcategory']
        image = request.FILES['image']
        slot = request.POST['slot']
        subcategory = SubCategory(
            category_name=title,
            category=Category.objects.get(uid= subcat),
            subcategory_image= image,
            no_of_slot=slot
        )
        subcategory.save()

    category = Category.objects.all()
    sub_category = SubCategory.objects.all()
    context = {'sub_category':sub_category,'category':category}
    return render(request,'adminpannel/pages/addsubcategory.html',context)


@login_required(login_url="adminlogin")
def updatesubcategory(request):
    if request.method == "POST":
        sc_uid = request.POST['sc_uid']
        title = request.POST['title']
        subcat = request.POST['subcategory']
        
        slot = request.POST['slot']
        subcategory = SubCategory.objects.get(uid= sc_uid)

        subcategory.category_name=title
        subcategory.category=Category.objects.get(uid= subcat)
        subcategory.no_of_slot=slot
        try:
            image = request.FILES['image']
            subcategory.subcategory_image= image
        except Exception as e:
            pass
        subcategory.save()
        return redirect('addsubcategory')



@login_required(login_url="adminlogin")
def addsubcategoryimage(request):
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method =="POST":
        sc_uid = request.POST['sc_uid']
        image = request.FILES['image']
        subcat = SubCategoryImage(
            subcategory = SubCategory.objects.get(uid= sc_uid),
            image = image
        )
        subcat.save()
        return redirect('addsubcategory')


@login_required(login_url="adminlogin")
def delsubcategory(request,uid):
    user_obj =request.user
    if request.user.is_superuser != True:
        return redirect('/')
    subcategory = SubCategory.objects.get(uid=uid)
    subcategory.delete()
    return redirect('addsubcategory')


@login_required(login_url="adminlogin")
def delsubcategoryimage(request,uid):
    if request.user.is_superuser != True:
        return redirect('/')
    subcategory = SubCategoryImage.objects.get(uid=uid)
    subcategory.delete()
    return redirect('addsubcategory')


@login_required(login_url="adminlogin")
def addproduct(request):
    user_obj =request.user
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method =='POST':
        title = request.POST['title']
        subcategory = request.POST['subcategory']
        mrp_price = request.POST['mrp_price']
        dis_price = request.POST['dis_price']
        image = request.FILES['image']
        desc = request.POST['desc']
        product = Product(
            product_name=title,
            sub_category=SubCategory.objects.get(uid=subcategory),
            mrp_price=mrp_price,
            dis_price=dis_price,
            product_description=desc,
            is_publish=True,
            image=image
        )
        product.save()
        return redirect('allproduct')
    sub_category = SubCategory.objects.all()
    context={'sub_category':sub_category}
    return render(request,'adminpannel/pages/addproduct.html',context)


@login_required(login_url="adminlogin")
def editproduct(request,uid):
    user_obj =request.user
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method == "POST":
        title = request.POST['title']
        subcategory = request.POST['subcategory']
        mrp_price = request.POST['mrp_price']
        dis_price = request.POST['dis_price']
        desc = request.POST['desc']
        image = request.FILES.get('image')    
        product = Product.objects.get(uid = uid)
        product.product_name=title
        product.sub_category=SubCategory.objects.get(uid=subcategory)
        product.mrp_price=mrp_price
        product.dis_price=dis_price
        product.product_description=desc 
        if image:
            product.image = image
        product.save()

    product = Product.objects.get(uid = uid)
    sub_category = SubCategory.objects.all()
    context={'sub_category':sub_category,'product':product}
    return render(request,'adminpannel/pages/editproduct.html',context)


@login_required(login_url="adminlogin")
def addproductimage(request,uid):
    user_obj =request.user
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method == "POST":
        product = Product.objects.get(uid = uid)
        print(product)
        image = request.FILES['image']
        product_images = ProductImage(
            product= product,
            image = image
        )
        product_images.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="adminlogin")
def delproductimage(request,uid):
    user_obj =request.user
    if user_obj.is_staff != True:
                return redirect('adminlogin')
    image = ProductImage.objects.get(uid=uid)
    image.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="adminlogin")
def delproduct(request,uid):
    user_obj =request.user
    if user_obj.is_staff != True:
                return redirect('adminlogin')
    product = Product.objects.get(uid=uid)
    print(product)
    product.delete()
    return redirect('allproduct')



@login_required(login_url="adminlogin")
def allproduct(request):
    user_obj =request.user
    if user_obj.is_staff != True:
        return redirect('adminlogin')
    product = Product.objects.all()
    context = {'product':product}
    return render(request,'adminpannel/pages/allproduct.html',context)


def addtimeslot(request,uid):
    sub_cat = SubCategory.objects.get(uid=uid)
    if request.method=="POST":
        time = request.POST['time']
        ts = TimeSlot(
            service=sub_cat,
            start_time=time,end_time=time
        )
        ts.save()
    timeslot = TimeSlot.objects.filter(service__uid =uid)
    context ={'timeslot':timeslot,'sub_cat':sub_cat}
    return render(request,'adminpannel/pages/addtimeslot.html',context)


def deltimeslot(request,uid):
    ts = TimeSlot.objects.get(uid=uid)
    sub_cat = SubCategory.objects.get(uid=ts.service.uid)
    ts.delete()
    return redirect('addtimeslot',sub_cat.uid)


def viewscityservice(request):
    cityser = CityService.objects.all()
    context = {'cityser':cityser}
    return render(request,'adminpannel/pages/cityservice.html',context)

def addcity(request):
    form = CityServiceModelForm(request.POST or None)
    print(form)
    if form.is_valid():
        # save the form data to model
        form.save()
        messages.success(request,"City Service Added Successfully")
    cityser = CityService.objects.all()
    context = {'cityser':cityser,'form':form}
    return render(request,'adminpannel/pages/addcity.html',context)


def editcityservice(request,uid):
    cityser = CityService.objects.get(uid=uid)
    form = CityServiceModelForm(request.POST or None,instance = cityser)
    if form.is_valid():
        # save the form data to model
        form.save()
    else:
        form = CityServiceModelForm(instance = cityser)
    context = {'form':form}
    return render(request,'adminpannel/pages/editcityservice.html',context)


def delcityservice(request,uid):
    cityser = CityService.objects.get(uid=uid)
    cityser.delete()
    return redirect('viewscityservice')


@login_required(login_url="adminlogin")
def change_status(request):
    change_type = request.GET.get('type')
    uid = request.GET.get('uid')
    if change_type =="category":
        category = Category.objects.get(uid=uid)
        if category.is_publish == True:
            category.is_publish =False
        else:
            category.is_publish =True
        category.save()
    elif change_type =="subcategory":
        subcategory = SubCategory.objects.get(uid=uid)
        if subcategory.is_publish == True:
            subcategory.is_publish =False
        else:
            subcategory.is_publish =True
        subcategory.save()
    elif change_type =="brands":
        brands = Brands.objects.get(uid=uid)
        if brands.is_publish == True:
            brands.is_publish =False
        else:
            brands.is_publish =True
        brands.save()
    elif change_type =="product":
        product = Product.objects.get(uid=uid)
        if product.is_publish == True:
            product.is_publish =False
        else:
            product.is_publish =True
        product.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

def contactform(request):
    contact = Contact.objects.all()
    context ={'contact':contact}
    return render(request,'adminpannel/pages/contactform.html',context)


def delcontact(request,id):
    cont = Contact.objects.get(id=id)
    cont.delete()
    return redirect('contactform')


def reqestimate(request):
    estim = Estimate.objects.all()
    context = {'estim':estim}
    return render(request,'adminpannel/pages/reqestimate.html',context)


def delreqestimate(request,id):
    if request.user.is_superuser != True:
        return redirect('/')
    cont = Estimate.objects.get(id=id)
    cont.delete()
    return redirect('reqestimate')


def new_account_req(request):
    if request.user.is_superuser != True:
        return redirect('/')
    new_account = NewAccount.objects.all()
    context = {"new_account":new_account}
    return render(request,'adminpannel/pages/newaccountrequest.html',context)




# cancel accepted start from here


def pending(request):
    user = request.user
    if (user.is_superuser == True) or (user.is_subadmin == True):
        pass
    else:
        return redirect('/')
    if request.method =="POST":
        booking_uid = request.POST['booking_uid']
        staff = request.POST['staff']
        staff_obj = User.objects.get(id =staff)
        try:
            booking = Booking.objects.get(uid=booking_uid)
            booking.assign_work = User.objects.get(id =staff)
            booking.save()
            messages.success(request," assign work to user successfully")
            if staff_obj.expo_token:
                send_push_notification(staff_obj.expo_token,"CASAXPRT STAFF NOTIFICATION","A work assign to you please check app")
        except IntegrityError as e:
            messages.error(request,"Already assign work to user")
    if user.is_subadmin:
        all_service_area= user.subadmin_service_area.all().values('city_name')
        booking = Booking.objects.filter(staff_status="Pending").filter(status="Pending").filter(assign_work=None).filter(city__in=Subquery(all_service_area))
    else:
        booking = Booking.objects.filter(staff_status="Pending").filter(status="Pending").filter(assign_work=None)
    context = {'booking':booking}
    return render(request,'adminpannel/ordersummery/pending.html',context)


def assignwork(request):
    user=request.user
    if (user.is_superuser == True) or (user.is_subadmin == True):
        pass
    else:
        return redirect('/')
    if request.method =="POST":
        booking_uid = request.POST['booking_uid']
        staff = request.POST['staff']
        staff_obj = User.objects.get(id =staff)
        try:
            booking = Booking.objects.get(uid=booking_uid)
            booking.assign_work = User.objects.get(id =staff)   
            booking.save()
            if staff_obj.expo_token:
                send_push_notification(staff_obj.expo_token,"CASAXPRT STAFF NOTIFICATION","A work assign to you please check app")
            messages.success(request," assign work to user successfully")
        except IntegrityError as e:
            messages.error(request,"Already assign work to user")
    if user.is_subadmin:
        all_service_area= user.subadmin_service_area.all().values('city_name')
        booking = booking = Booking.objects.filter(staff_status="Pending").filter(status="Pending").filter(assign_work__isnull=False).filter(city__in=Subquery(all_service_area))
    else:
        booking = booking = Booking.objects.filter(staff_status="Pending").filter(status="Pending").filter(assign_work__isnull=False)
    
    context = {'booking':booking}
    return render(request,'adminpannel/ordersummery/assignwork.html',context)


def accepted(request):
    user=request.user
    if (user.is_superuser == True) or (user.is_subadmin == True):
        pass
    else:
        return redirect('/')
    if request.method =="POST":
        booking_uid = request.POST['booking_uid']
        staff = request.POST['staff']
        staff_obj = User.objects.get(id =staff)
        try:
            booking = Booking.objects.get(uid=booking_uid)
            booking.assign_work = User.objects.get(id =staff)
            booking.staff_status = "Pending"
            booking.save()
            if staff_obj.expo_token:
                send_push_notification(staff_obj.expo_token,"CASAXPRT STAFF NOTIFICATION","A work assign to you please check app")
            messages.success(request," assign work to user successfully")
        except IntegrityError as e:
            messages.error(request,"Already assign work to user")
    if user.is_subadmin:
        all_service_area= user.subadmin_service_area.all().values('city_name')
        booking = Booking.objects.filter(staff_status="Accepted").filter(status="Pending").filter(assign_work__isnull=False).filter(city__in=Subquery(all_service_area))
    else:
        booking = Booking.objects.filter(staff_status="Accepted").filter(status="Pending").filter(assign_work__isnull=False)
    context = {'booking':booking}
    return render(request,'adminpannel/ordersummery/accepted.html',context)


def completed(request):
    user =request.user
    if (user.is_superuser == True) or (user.is_subadmin == True):
        pass
    else:
        return redirect('/')
    if request.method =="POST":
        booking_uid = request.POST['booking_uid']
        staff = request.POST['staff']
        staff_obj = User.objects.get(id =staff)
        try:
            booking = Booking.objects.get(uid=booking_uid)
            booking.assign_work = User.objects.get(id =staff)
            booking.save()
            if staff_obj.expo_token:
                send_push_notification(staff_obj.expo_token,"CASAXPRT STAFF NOTIFICATION","A work assign to you please check app")
            messages.success(request," assign work to user successfully")
        except IntegrityError as e:
            messages.error(request,"Already assign work to user")
    if user.is_subadmin:
        all_service_area= user.subadmin_service_area.all().values('city_name')
        booking = Booking.objects.filter(staff_status="Completed").filter(status="Completed").filter(assign_work__isnull=False).filter(city__in=Subquery(all_service_area))
    else:
        booking = Booking.objects.filter(staff_status="Completed").filter(status="Completed").filter(assign_work__isnull=False)
    context = {'booking':booking}
    return render(request,'adminpannel/ordersummery/completed.html',context)


def staff_cancel(request):
    user = request.user
    if (user.is_superuser == True) or (user.is_subadmin == True):
        pass
    else:
        return redirect('/')
    if request.method =="POST":
        booking_uid = request.POST['booking_uid']
        staff = request.POST['staff']
        staff_obj = User.objects.get(id =staff)
        try:
            booking = Booking.objects.get(uid=booking_uid)
            booking.assign_work = User.objects.get(id =staff)
            booking.staff_status = "Pending"
            booking.save()
            if staff_obj.expo_token:
                send_push_notification(staff_obj.expo_token,"CASAXPRT STAFF NOTIFICATION","A work assign to you please check app")
            messages.success(request," assign work to user successfully")
        except IntegrityError as e:
            messages.error(request,"Already assign work to user")
    if user.is_subadmin:
        all_service_area= user.subadmin_service_area.all().values('city_name')
        booking = Booking.objects.filter(staff_status="Canceled").filter(status="Pending").filter(assign_work__isnull=False).filter(city__in=Subquery(all_service_area))
    else:
        booking = Booking.objects.filter(staff_status="Canceled").filter(status="Pending").filter(assign_work__isnull=False)
    context = {'booking':booking}
    return render(request,'adminpannel/ordersummery/staff-cancel.html',context)


def allbooking(request):
    user = request.user
    if user.is_subadmin:
        all_service_area= user.subadmin_service_area.all().values('city_name')
        booking = Booking.objects.filter(city__in=Subquery(all_service_area))
    else:
        booking = Booking.objects.all()
    context = {'booking':booking}
    return render(request,'adminpannel/ordersummery/allbookings.html',context)

def client_cancel(request):
    user =request.user
    if (user.is_superuser == True) or (user.is_subadmin == True):
        pass
    else:
        return redirect('/')
    if request.method =="POST":
        booking_uid = request.POST['booking_uid']
        staff = request.POST['staff']
        staff_obj = User.objects.get(id =staff)
        try:
            booking = Booking.objects.get(uid=booking_uid)
            booking.assign_work = User.objects.get(id =staff)
            booking.save()
            if staff_obj.expo_token:
                send_push_notification(staff_obj.expo_token,"CASAXPRT STAFF NOTIFICATION","A work assign to you please check app")
            messages.success(request," assign work to user successfully")
        except IntegrityError as e:
            messages.error(request,"Already assign work to user")
    if user.is_subadmin:
        all_service_area= user.subadmin_service_area.all().values('city_name')
        booking = booking = Booking.objects.filter(staff_status="Canceled").filter(status="Canceled").filter(city__in=Subquery(all_service_area))
    else:
        booking = Booking.objects.filter(staff_status="Canceled").filter(status="Canceled")
    context = {'booking':booking}
    return render(request,'adminpannel/ordersummery/canceled.html',context)


def newstaffaccount(request):
    if request.user.is_superuser != True:
        return redirect('/')
    newaccount = NewAccount.objects.all()
    context = {'newaccount':newaccount}
    return render(request,'adminpannel/pages/newstaffaccount.html',context)


def managestaff(request):
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method =="POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        staff_obj =User.objects.filter(phone_number=phone).first()
        if staff_obj:
            staff_obj.is_staff=True
            staff_obj.save()
            return redirect('add_staff',staff_obj.id)
        staff = User(
            full_name = name,
            phone_number = phone,
            email = email,
            is_staff=True
        )
        staff.save()
        return redirect('add_staff',staff.id)
    staff = User.objects.filter(is_staff= True)
    context = {'staff':staff}
    return render(request,'adminpannel/pages/managestaff.html',context)


def managesubadmin(request):
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method =="POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        subadmin_obj =User.objects.filter(phone_number=phone).first()
        if subadmin_obj:
            subadmin_obj.is_subadmin=True
            subadmin_obj.save()
            return redirect('managesubadmin')
        staff = User(
            full_name = name,
            phone_number = phone,
            email = email,
            is_subadmin=True
        )
        staff.save()
        return redirect('managesubadmin')
    staff = User.objects.filter(is_subadmin= True)
    servicearea = CityService.objects.all()
    context = {'staff':staff,'servicearea':servicearea}
    return render(request,'adminpannel/pages/managesubadmin.html',context)


def addservicearea(request):
    if request.method=="POST":
        uid = request.POST['uid']
        city = request.POST['city']
        servicearea = SubAdminServiceArea(
            user = User.objects.get(id=uid),
            city_name= city
        )
        servicearea.save()
    return redirect('managesubadmin')


def delservicearea(request,uid):
    servicearea = SubAdminServiceArea.objects.get(uid=uid)
    servicearea.delete()
    return redirect('managesubadmin')


def editsubadmin(request):
    if request.method =="POST":
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST.get('password')

        subadmin_obj =User.objects.filter(phone_number=phone_number).first()
        subadmin_obj.full_name = name
        subadmin_obj.email = email
        if password:
            subadmin_obj.password = make_password(password)
        subadmin_obj.save()
    return redirect('managesubadmin')


def add_address(request):
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method == "POST":
        uid = request.POST['uid']
        name = request.POST['name']
        addressline = request.POST['addressline']
        locality = request.POST['locality']
        city = request.POST['city']
        zipcode = request.POST['zipcode']
        state = request.POST['state']
        phone = request.POST['phone']
        email = request.POST['email']
        try:
            address = Address.objects.get(user_id =uid)
            address.name = name
            address.addressline = addressline
            address.locality = locality
            address.city = city
            address.zipcode = zipcode
            address.state = state
            address.phone= phone
            address.email =email
            address.save()
        except Address.DoesNotExist:
            address= Address(
                user=User.objects.get(id=uid),
                name=name,addressline=addressline,locality=locality,city=city,zipcode=zipcode,
                state=state,phone=phone,email=email
                ) 
            address.save()
        user=User.objects.get(id=uid)  
        if user.is_staff==True: 
            return redirect('add_staff',uid)
        if user.is_subadmin==True:
            return redirect('managesubadmin')
        return redirect('viewuserdetails',uid)


def add_staff(request,uid):
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method == "POST":
        full_name = request.POST['full_name']
        uid = request.POST['uid']
        email = request.POST['email']
        user = User.objects.get(id=uid)
        user.full_name =full_name
        user.email=email
        user.save()
    staff = User.objects.get(id=uid)
    sub_cat = SubCategory.objects.all()
    context = {'staff':staff,'sub_cat':sub_cat}    
    return render(request,'adminpannel/pages/addstaff.html',context)


def add_staf_work_type(request):
    if request.user.is_superuser != True:
        return redirect('/')
    if request.method =="POST":
        staff_uid = request.POST['uid']
        sub_cat_uid = request.POST['sub_cat_uid']
        sub_cat = StaffWorkType.objects.filter(uid=sub_cat_uid).first()
        print("sub_cat",sub_cat)
        if sub_cat:
            return redirect('add_staff',staff_cat)
        else:
            worktype = StaffWorkType(
                user = User.objects.get(id=staff_uid),
                sub_category= SubCategory.objects.get(uid=sub_cat_uid)
            )
        worktype.save()
        return redirect('add_staff',staff_uid)


def del_staf_work_type(request,uid):
    if request.user.is_superuser != True:
        return redirect('/')
    sub_cat = StaffWorkType.objects.get(uid=uid)
    user_uid = sub_cat.user.id
    sub_cat.delete()
    return redirect('add_staff',user_uid)



def estimate(request):
    if request.user.is_superuser != True:
        return redirect('/')
    est = Estimate.objects.all()
    context ={'est':est}
    return render(request,'adminpannel/pages/estimate.html',context)


def delestimate(request,id):
    if request.user.is_superuser != True:
        return redirect('/')
    est = Estimate.objects.get(id=id)
    est.delete()
    return redirect('estimate')


def userdetails(request):
    if request.user.is_superuser != True:
        return redirect('/')
    userdet = User.objects.filter(is_superuser = False)
    context ={'userdet':userdet}
    return render(request,'adminpannel/pages/userdetails.html',context)


def viewuserdetails(request,uid):
    if request.user.is_superuser != True:
        return redirect('/')
    userdet = User.objects.get(id=uid)
    context ={'userdet':userdet}
    return render(request,'adminpannel/pages/viewuserdetails.html',context)


def managepage(request):
    if request.method =="POST":
        servicename = request.POST['servicename']
        service = Service(
            service_name=servicename
        )
        service.save()

    service_name = Service.objects.all()
    serviceuid = request.GET.get('serviceuid')
    try:
        oneservice = Service.objects.get(uid=serviceuid)
    except Service.DoesNotExist:
        oneservice={}
    allcategory = Category.objects.all()
    servicep =ServiceProduct.objects.filter(service__uid=serviceuid)
    context ={'service_name':service_name,'servicep':servicep,'oneservice':oneservice,'allcategory':allcategory}
    return render(request,'adminpannel/pages/managepage.html',context)


def delservicename(request,uid):
    service_name = Service.objects.get(uid=uid)
    service_name.delete()
    return redirect('managepage')


def addserviceproduct(request):
    if request.method =="POST":
        serviceuid = request.POST['serviceuid']
        categoryuid = request.POST['categoryuid']
        productuid = request.POST['productuid']
        servicep = ServiceProduct(
            service = Service.objects.get(uid=serviceuid),
            product = Product.objects.get(uid=productuid),
            category= Category.objects.get(uid=categoryuid)
        )
        servicep.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def delserviceproduct(request,uid):
    servicep = ServiceProduct.objects.get(uid=uid)
    servicep.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def getallproduct(request):
    cat = request.GET.get('cat')
    print(cat)
    if cat:
        try:
            prod = Product.objects.filter(sub_category__category__uid=cat).values()
            print(prod)
        except ValueError:
            # Handle the case where 'cat' is not a valid integer
            prod = {}
    else:
        prod = {}
    return JsonResponse(list(prod), safe=False)


#Add Manually user 

def checkusernumber(request):
    if request.method =="POST":
        phone_number = request.POST['phone_number']
        user_obj,created = User.objects.get_or_create(phone_number=phone_number)
        print(user_obj)
        print(created)
        return redirect('addbooking',phone_number)


def addbooking(request,num):
    if request.method == "POST":
        name = request.POST['full_name']
        saddress = request.POST['addressline']
        locality = request.POST['locality']
        city = request.POST['city']
        zipcode = request.POST['zipcode']
        state = request.POST['state']
        phone = request.POST['phone']
        email = request.POST['email']
        try:
            address=Address(user=User.objects.get(phone_number=num),name=name,addressline=saddress,locality=locality,city=city,zipcode=zipcode,
                                 state=state,phone=phone,email=email)
            address.save()
        except IntegrityError as e:
            address= Address.objects.get(user=User.objects.get(phone_number=num))
            address.name = name
            address.addressline = saddress
            address.locality = locality
            address.city = city
            address.zipcode = zipcode
            address.state = state
            address.phone= phone
            address.email =email
            address.save()
    cat = request.GET.get('category')
    if cat:
        sub_cat = SubCategory.objects.get()
    try:
        user_obj = User.objects.get(phone_number=num)
    except User.DoesNotExist:
        pass
    booking = Booking.objects.filter(user = user_obj)[:5]
    context = {'user_obj':user_obj,'booking':booking}
    return render(request,'adminpannel/ordersummery/addbooking.html',context)


def getsubcategory(request):
    category = request.GET.get('cat')
    print(category)
    if category:
        try:
            subcategory = SubCategory.objects.filter(category__uid=category).values()
            print(subcategory)
        except ValueError:
            # Handle the case where 'category' is not a valid integer
            subcategory = {}
    else:
        subcategory = {}
    return JsonResponse(list(subcategory), safe=False)


def createbookingmanually(request,mob):
    user_obj = User.objects.get(phone_number=mob)
    if request.method =="POST":
        pass
    category = Category.objects.all()
    context = {'category':category,'user_obj':user_obj}
    return render(request,'adminpannel/ordersummery/createbooking.html',context)


def select_data_time_slot(request,mob,subcat):
    if request.method == "POST":
        phone_number = request.POST['phone']
        booking_date = request.POST['booking_date']
        time_slot= request.POST['time_slot']
        print(booking_date)
        print(time_slot)
        user_obj=User.objects.get(phone_number=phone_number)
        booking= Booking(
            user =user_obj ,
            booking_time = booking_date,
            time_slot=TimeSlot.objects.get(uid=time_slot),
            is_paid=False,
            name=user_obj.address.name,addressline=user_obj.address.addressline,locality=user_obj.address.locality,
            city=user_obj.address.city,zipcode=user_obj.address.zipcode,
            state=user_obj.address.state,phone=user_obj.address.phone,email=user_obj.address.email
        )
        booking.save()
        return redirect('addbookingproduct',booking.uid)
    try:
        sub_cat = SubCategory.objects.get(uid=subcat)
        sdate = request.GET.get('sdate')  
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
        current_time_utc = timezone.now()
        local_time = timezone.localtime(current_time_utc)
        local_time_plus_2_hours = local_time + timedelta(hours=2)
        local_time_str = local_time_plus_2_hours.strftime('%H:%M:%S')
        local_time_obj = datetime.strptime(local_time_str, '%H:%M:%S').time()
        for t in time_slot:
            print(type(local_time_obj))
            get_booking = Booking.objects.filter(time_slot__service=sub_cat).filter(booking_time =act_date).filter(time_slot=t).count()
            if get_booking < sub_cat.no_of_slot:
                if act_date ==current_date.strftime("%Y-%m-%d") and t.start_time <= local_time_obj :
                    t.availble=False
                else:
                    t.availble=True        
            else:
                t.availble=False
        context={'next_four_days':next_four_days,"time_slot":time_slot,'sub_cat':sub_cat,'mob':mob,'act_date':act_date}
        return render(request,'adminpannel/ordersummery/selectdateandtimeslot.html',context)
    except SubCategory.DoesNotExist:
        return redirect('createbookingmanually',mob)


def addbookingproduct(request,uid):
    booking = Booking.objects.get(uid=uid)
    if request.method=="POST":
        product_uid = request.POST['product']
        book = BookingProduct(
            booking=booking,
            product = Product.objects.get(uid=product_uid),
            quantity=1
        )
        book.save()
    product =Product.objects.filter(sub_category__uid=booking.time_slot.service.uid)
    context ={'booking':booking,'product':product}
    return render(request,'adminpannel/ordersummery/addbookingproduct.html',context)


def delbookingproduct(request,uid):
    p = BookingProduct.objects.get(uid=uid)
    buid= p.booking.uid
    p.delete()
    return redirect('addbookingproduct',buid)