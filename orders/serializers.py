from rest_framework import serializers
from .models import OrderModel, OrderAssortmentTableModel
from assortment.models import AssortmentModel
from assortment.serializers import AssortmentSerializer
from organizations.models import OrganizationModel
from organizations.serializers import OrganizationSerializer
 

class OrderListSerializer(serializers.ModelSerializer):
    org_name = serializers.StringRelatedField(source='organization')

    class Meta:
        model = OrderModel
        fields = ['uuid', 'number', 'date', 'organization', 'org_name', 'comment', 'summa']


class OrderAssortmentTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAssortmentTableModel
        fields = ['num', 'assortment', 'count', 'price', 'summa']    
          
class OrderSerializer(serializers.ModelSerializer):
    table = OrderAssortmentTableSerializer(many=True)  # Вложенный сериализатор
    org_name = serializers.StringRelatedField(source='organization')

    class Meta:
        model = OrderModel
        fields = ['uuid', 'number', 'date', 'organization', 'org_name', 'comment', 'summa', 'table'] 
        # extra_kwargs = {'table': {'required': False}}
 

#Special serialize for all data
class OrderDialogSerializer(serializers.ModelSerializer):
    table = OrderAssortmentTableSerializer(many=True)  # Вложенный сериализатор
    org_name = serializers.StringRelatedField(source='organization')
    all_organizations = serializers.SerializerMethodField()
    all_assortment = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderModel
        fields = ['uuid', 'number', 'date', 'organization', 'org_name', 'comment', 'summa', 'table','all_organizations', 'all_assortment']       

    def get_all_organizations(self, obj):
        orgs = OrganizationSerializer( OrganizationModel.objects.all(),many=True)
        return orgs.data
    
    def get_all_assortment(self, obj):
        assortments = AssortmentSerializer( AssortmentModel.objects.all(),many=True)
        return assortments.data
        