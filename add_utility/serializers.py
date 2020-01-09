from rest_framework import serializers
from .models import UtilityList

class LoadWalletSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=250)
    service = serializers.CharField(max_length=250)
    description = serializers.CharField(max_length=250)

    class Meta:
        model = UtilityList
        fields = ['name', 'service', 'description']