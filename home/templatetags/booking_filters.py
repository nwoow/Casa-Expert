from django import template

register = template.Library()

@register.filter
def filter_by_status(bookings, status):
    return bookings.filter(status=status)