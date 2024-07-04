from django.urls import path
from . import views

urlpatterns=[ 
    path('register/',views.register,name='register'),
    path('user-login/',views.user_login,name='user_login'),
    path('staff-login/',views.staff_login,name='staff_login'),
    path('set-message-token/',views.set_message_token),
    path('verify-otp/',views.verify_otp,name='verify_otp'),
    path('profile/',views.profile),
    path('updateprofile/',views.updateprofile),

    path('show-home-data',views.show_home_data),
    path('show-category/',views.show_category),
    path('search-view/',views.search_view),
    path('show-subcategory/<uid>',views.show_subcategory),
    path('get-subcategory/<uid>',views.get_subcategory),
    path('service/<uid>',views.service),
    path('address/',views.address),
    path('del-address/',views.del_address),
    path('time-slot/<uid>',views.time_slot),
    path('orderlist/',views.orderlist),
    path('cancel-booking/',views.cancel_booking),
    path('product-reviews/',views.product_reviews),

    path('staff-status-work/',views.staff_status_work),
    path('staff-change-status/',views.staff_change_status),

    path('send-staff-work-otp/',views.send_staff_work_otp),

    path('reject-reason/',views.reject_reason),
    path('generate-booking/',views.generate_booking),

    path('get-booked-product/<uid>',view.get_booked_product)
    path('change-booked-product/',views.change_booked_product),
    path('change-booked-product-status/',views.change_booked_product_status)

]