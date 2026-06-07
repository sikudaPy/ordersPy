from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from .models import OrderModel 
from organizations.models import ManagerModel
from .forms import OrderAssortFormSet, OrderForm
from django.contrib.auth import login, logout, authenticate
from .forms import LoginForm
from django.db.models import Q

from .serializers import OrderSerializer
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)     
                return redirect('/orders')  
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/') 


def get_organization_by_request(request):
    org = None
    if request.user.is_authenticated:
        manager = ManagerModel.objects.filter(user=request.user).first()
        if manager != None:
           org = manager.organization
    return org       

def get_orders_by_request(request, org=None):
    if org == None:
        org = get_organization_by_request(request)

    strFind = request.GET.get("strFind") or ""
    if request.user.is_superuser:
        orders = getOrdersByFilter(strFind)
    else:
        if org == None:
            orders = OrderModel.objects.none()
        else:
            orders = getOrdersByFilter(strFind).filter(organization=org)       
    return orders        

def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        return redirect('/orders/new')    

    theme= request.GET.get("theme") or "auto"
    strFind = request.GET.get("strFind") or ""

    org = get_organization_by_request(request)
    orders = get_orders_by_request(request, org)
    template = loader.get_template('orders_all.html')
    
    context = {
        'title': "Заказы для организации: "+"Все организации" if org is None else org.name,
        'context': orders,
        'theme': theme,
        'strFind': strFind
    }
    return HttpResponse(template.render(context, request))

def order_new(request):
    org = get_organization_by_request(request)
    if request.method == 'POST':
        order_save(request)
        return redirect('/orders')
    else:
        order_form = OrderForm(org=org)
        assort_formset = OrderAssortFormSet()
        return render(request, 'order_all_item.html', 
                      {
                          'order_form': order_form,
                          'assort_formset': assort_formset
                      })             

def order_edit(request, pk):
    org = get_organization_by_request(request)
    order = OrderModel.objects.get(pk=pk)
    if request.method == 'POST':
        order_save(request, order)
        return redirect('/orders')
    else:
        order_form = OrderForm(instance=order, org=org)
        assort_formset = OrderAssortFormSet(instance=order)
        return render(request, 'order_all_item.html',
                      {
                          'order_form': order_form,
                          'assort_formset': assort_formset
                      })

def order_save(request, order=None):
    org = get_organization_by_request(request)
    if order is None:
        order_form = OrderForm(request.POST)
        assort_formset = OrderAssortFormSet(request.POST)
    else:
        order_form = OrderForm(request.POST, instance=order)     
        assort_formset = OrderAssortFormSet(request.POST, instance=order)

    #assorts = assort_formset.save(commit=False)
    
    if order_form.is_valid() and assort_formset.is_valid():

        if org is None:
            order = order_form.save()
        else: 
            order = order_form.save(commit=False)
            order.organization = org
            order.save()

        order.summa = 0
        for item in assort_formset.cleaned_data:
            if bool(item) and item['DELETE'] == False:
                order.summa += item['summa']
        order.save()    

        assorts = assort_formset.save(commit=False)
        for item in assorts:
            item.order = order
            item.save()

        for item in assort_formset.deleted_objects:
            item.delete()    

def order_del(request, pk):   
    if request.method == 'POST':
        order = OrderModel.objects.get(pk=pk)
        if order is not None:
            order.delete()
    return redirect('/orders')

def order_root(request):
    return redirect('orders/') 

#Special functions -----------------------------------------------------------------------------------------    
def getOrdersByFilter(strFind: str = ""):
    return OrderModel.objects.filter(
        Q(number__icontains=strFind) | 
        Q(date__icontains=strFind) |
        Q(organization__name__icontains=strFind) |
        Q(comment__icontains=strFind) |
        Q(summa__icontains=strFind) 
        ).order_by('date') 

#API functions -----------------------------------------------------------------------------------------    
class OrdersListAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
         articles = OrderModel.objects.all()
         serializer = OrderSerializer(articles, many=True)
         return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        # if serializer.uuid == "":
        #     serializer.uuid = uuid.uuid4()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class OrdersAPI(APIView):
#     #permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request, pk, format=None):
#         order = OrderModel.objects.get(pk=pk)
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         order = OrderModel.objects.get(pk=pk)
#         serializer = OrderSerializer(order, data=request.DATA)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         order = OrderModel.objects.get(pk=pk)
#         order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
