from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminlogin,name='adminlogin'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('contactform',views.contactform,name='contactform'),
    path('delcontact/<id>',views.delcontact,name='delcontact'),

    path('addcategory',views.addcategory,name='addcategory'),
    path('delcategory/<uid>',views.delcategory,name='delcategory'),
    path('addsubcategory',views.addsubcategory,name='addsubcategory'),
    path('updatesubcategory',views.updatesubcategory,name='updatesubcategory'),
    path('addsubcategoryimage',views.addsubcategoryimage,name='addsubcategoryimage'),
    path('delsubcategory/<uid>',views.delsubcategory,name='delsubcategory'),
    path('delsubcategoryimage/<uid>',views.delsubcategoryimage,name='delsubcategoryimage'),

    path('addproduct',views.addproduct,name='addproduct'),
    path('editproduct/<uid>',views.editproduct,name='editproduct'),
    path('addproductimage/<uid>',views.addproductimage,name='addproductimage'),
    path('delproduct/<uid>',views.delproduct,name='delproduct'),
    path('delproductimage/<uid>',views.delproductimage,name='delproductimage'),
    path('allproduct',views.allproduct,name='allproduct'),

    path('addtimeslot/<uid>',views.addtimeslot,name='addtimeslot'),
    path('deltimeslot/<uid>',views.deltimeslot,name='deltimeslot'),
    path('viewscityservice',views.viewscityservice,name='viewscityservice'),
    path('addcity',views.addcity,name='addcity'),
    path('editcityservice/<uid>',views.editcityservice,name='editcityservice'),
    path('delcityservice/<uid>',views.delcityservice,name='delcityservice'),

    path('change-status',views.change_status,name='change_status'),

    path('pending',views.pending,name="pending"),
    path('assignwork',views.assignwork,name='assignwork'),
    path('accepted',views.accepted,name='accepted'),
    path('completed',views.completed,name='completed'),
    path('staff-cancel',views.staff_cancel,name='staff_cancel'),
    path('client-cancel',views.client_cancel,name='client_cancel'),

    path('newstaffaccount',views.newstaffaccount,name="newstaffaccount"),
    path('managestaff',views.managestaff,name='managestaff'),
    path('add-address',views.add_address,name='add_address'),
    path('add-staf-work-type',views.add_staf_work_type,name="add_staf_work_type"),
    path('del-staf-work-type/<uid>',views.del_staf_work_type,name="del_staf_work_type"),
    path('add-staff/<uid>',views.add_staff,name='add_staff'),
    path('estimate',views.estimate,name='estimate'),
    path('delestimate/<id>',views.delestimate,name='delestimate'),
    path('userdetails',views.userdetails,name='userdetails'),
    path('viewuserdetails/<uid>',views.viewuserdetails,name='viewuserdetails'),
    path('managepage',views.managepage,name='managepage'),
    path('delservicename/<uid>',views.delservicename,name='delservicename'),
    path('addserviceproduct',views.addserviceproduct,name='addserviceproduct'),
    path('getallproduct',views.getallproduct,name='getallproduct'),
    path('delserviceproduct/<uid>',views.delserviceproduct,name='delserviceproduct'),
]