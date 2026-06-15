from rest_framework import serializers
from .models import OrderModel, OrderAssortmentTableModel
from assortment.models import AssortmentModel
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
        fields = ['num', 'assortiment', 'count', 'price', 'summa']    
          
class OrderSerializer(serializers.ModelSerializer):
    table = OrderAssortmentTableSerializer(many=True)  # Вложенный сериализатор
    org_name = serializers.StringRelatedField(source='organization')

    class Meta:
        model = OrderModel
        fields = ['uuid', 'number', 'date', 'organization', 'org_name', 'comment', 'summa', 'table']  

#Spesial serialize for all data
class OrderDialogSerializer(serializers.ModelSerializer):
    table = OrderAssortmentTableSerializer(many=True)  # Вложенный сериализатор
    org_name = serializers.StringRelatedField(source='organization')
    all_organizations = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderModel
        fields = ['uuid', 'number', 'date', 'organization', 'org_name', 'comment', 'summa', 'table','all_organizations']       

    def get_all_organizations(self, obj):
        orgs = OrganizationSerializer( OrganizationModel.objects.all(),many=True)
        return orgs.data
        