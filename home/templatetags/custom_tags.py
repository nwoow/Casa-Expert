from django import template
from account.models import Booking
register = template.Library()


@register.filter
def get_cart_tag(service,sess_cart):
    cart_count_tag = 0
    if sess_cart:
        for k in sess_cart:
            if str(service.uid) == str(k):              
                cart_count_tag = sess_cart[k]
            else:
                pass
    return cart_count_tag


@register.simple_tag
def product_in_cart_check(service,sess_cart):
    if sess_cart:
        for k in sess_cart:
            if str(service.uid) == str(k): 
                return True
            return False
        return False   


@register.simple_tag
def timeslot_check(booking_date,time_slot):
    pass


   

    

