from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from rest_framework import serializers
from .models import LostFoundItem

class LostFoundItemSerializer(serializers.ModelSerializer):
    @extend_schema_field(OpenApiTypes.BINARY)
    def image(self):
        return self.fields['image']

    class Meta:
        model = LostFoundItem
        fields = '__all__'
        read_only_fields = ['created_at','user']

    def validate(self, data):
        status = data.get('status')
        user = self.context['request'].user

        if status=='lost' and (not user or not user.is_authenticated):
            raise serializers.ValidationError("You must be authenticated to report a lost item.")
        return data

    def create(self,validated_data):
        user=self.context['request'].user
        if validated_data['status']=='lost' or user.is_authenticated:
            validated_data['user']=user
        return super().create(validated_data)