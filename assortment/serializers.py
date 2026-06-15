from rest_framework import serializers
from .models import AssortmentModel

class AssortmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AssortmentModel
        fields = ['uuid', 'name']