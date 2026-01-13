from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path
#from rest_framework import permissions
#from drf_yasg.views import get_schema_view
#from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="My API",
#         default_version='v1',
#         description="Welcome to the awesome API documentation!",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="contact@local.local"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=(permissions.IsAuthenticated,),
# )

urlpatterns = [
    path('', views.order_root),
    path('orders/', views.order_list, name='orders'),
    path('orders/new/', views.order_new, name='orders'),
    path('orders/edit/<pk>/', views.order_edit, name='orders'),
    path('orders/del/<pk>/', views.order_del, name='orders'),
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    #path('accounts/profile/', views.order_root),
    #path('accounts/profile/orders', views.order_root),
    #path('orders-api/', views.OrdersListAPI.as_view(), name='article-api'),
    #path('orders-api/<pk>/', views.OrdersAPI.as_view(), name='article-api'),

    #path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    #path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),   
]