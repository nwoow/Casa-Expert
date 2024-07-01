from rest_framework import serializers
from . models import *




class AddressModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields ="__all__"



class UserModelSerializers(serializers.ModelSerializer):
    addressddet = AddressModelSerializers(source='address',
        many=False,
        read_only=True,
    )
    class Meta:
        model = User
        fields ="__all__"


class BookingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingProduct
        fields = ['product', 'quantity','uid']
        depth = 1


class BookingModelSerializers(serializers.ModelSerializer):
    booking_products = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = "__all__"
        depth = 1

    def get_booking_products(self, obj):
        booking_products = BookingProduct.objects.filter(booking=obj)
        return BookingProductSerializer(booking_products, many=True).data

class RejectReasonSerializers(serializers.ModelSerializer):

    class Meta:
        model =RejectReason
        fields = ['title']