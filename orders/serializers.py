from rest_framework import serializers
from .models import OrderModel, OrderAssortmentTableModel

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
