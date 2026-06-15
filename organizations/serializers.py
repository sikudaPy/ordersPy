from rest_framework import serializers
from .models import OrganizationModel

class OrganizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrganizationModel
        fields = ['uuid', 'name']