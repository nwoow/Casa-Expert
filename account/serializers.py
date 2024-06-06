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




class BookingModelSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Booking
        fields = "__all__"
        depth = 1


class RejectReasonSerializers(serializers.ModelSerializer):

    class Meta:
        model =RejectReason
        fields = ['title']