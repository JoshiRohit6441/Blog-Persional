from rest_framework import serializers
from .models import CountryCode, CountryModel, CityModal, StateModal


class CountryCodeSerialzier(serializers.ModelSerializer):
    class Meta:
        model = CountryCode
        fields = "__all__"


class CountryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryModel
        fields = "__all__"


class StateModalSerializer(serializers.ModelSerializer):
    country = CountryModelSerializer()

    class Meta:
        model = StateModal
        fields = "__all__"


class CityModalSerializer(serializers.ModelSerializer):
    Country = CountryModelSerializer()
    state = StateModalSerializer()

    class Meta:
        model = CityModal
        fields = "__all__"
