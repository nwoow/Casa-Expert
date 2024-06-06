from django.urls import path
from . import views

urlpatterns=[ 
    path('',views.home,name='home'),
    path('verifyotp',views.verifyotp,name='verifyotp'),
    path('ulogout',views.ulogout,name='ulogout'),
    path('service/<str:slug>',views.service,name='service'),
    path('add-to-cart',views.add_to_cart,name='add_to_cart'),
    path('deletesessioncart/<uid>',views.deletesessioncart,name='deletesessioncart'),
    path('checkout',views.checkout,name='checkout'),
    path('register-as-a-professional',views.register_as_a_professional,name='register_as_a_professional'),
    path('gallery',views.gallery,name='gallery'),
    path('contact',views.contact,name='contact'),
    path('userlogout',views.userlogout,name='userlogout'),
    path('cart',views.cart,name='cart'),
    path('address',views.address,name='address'),
    path('help',views.help,name='help'),
    path('order',views.order,name='order'),
    path('paymentcallback',views.paymentcallback,name='paymentcallback'),
    path('thankyou',views.thankyou,name='thankyou'),
    path('profile',views.profile,name='profile'),

    path('about',views.about,name='about'),
    path('faq',views.faq,name='faq'),
    path('privacy-policy',views.privacy_policy,name='privacy_policy'),
    path('terms-and-conds',views.terms_and_conds,name='terms_and_conds'),
]