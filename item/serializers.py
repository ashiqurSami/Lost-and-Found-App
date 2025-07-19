from rest_framework import serializers
from .models import LostFoundItem
from django.contrib.gis.geos import Point
from .utils import reverse_geocode

class LostFoundItemSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=False)
    longitude = serializers.FloatField(write_only=True, required=False)

    class Meta:
        model = LostFoundItem
        fields = '__all__'
        read_only_fields = ['created_at','user','point']

    def validate(self, data):
        status = data.get('status')
        user = self.context['request'].user

        if status=='lost' and (not user or not user.is_authenticated):
            raise serializers.ValidationError("You must be authenticated to report a lost item.")

        # 🔄 Fill location using reverse geocode BEFORE DRF complains
        lat = self.initial_data.get('latitude')
        lon = self.initial_data.get('longitude')

        if data.get('location') in [None, ''] and lat and lon:
            location = reverse_geocode(float(lat), float(lon))
            if location:
                data['location'] = location

        return data

    def create(self,validated_data):
        user=self.context['request'].user
        if validated_data['status']=='lost' or user.is_authenticated:
            validated_data['user']=user

        lat=validated_data.pop('latitude',None)
        lon=validated_data.pop('longitude',None)

        if lat is not None and lon is not None:
            validated_data['point']= Point(lon,lat)

            #if location is not provided by user
            if not validated_data.get('location'):
                location = reverse_geocode(lat, lon)
                if location:
                    validated_data['location'] = location

        return super().create(validated_data)

    def update(self, instance, validated_data):
        lat = validated_data.pop('latitude', None)
        lon = validated_data.pop('longitude', None)

        if lat is not None and lon is not None:
            instance.point = Point(lon, lat)

            # if location is not provided by user
            if not validated_data.get('location'):
                location = reverse_geocode(lat, lon)
                if location:
                    validated_data['location'] = location

        return super().update(instance,validated_data)