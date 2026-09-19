from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer,OrderDetailSerializer

from backend.mixins import AuthorizationMixin
from .models import Order,OrderDetail


class OrderViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("orders")
        if self.request.GET.get("marketplace"):
            marketplace=self.request.GET.get("marketplace")
            queryset=queryset.filter(marketplace=marketplace)
        search=None
        if self.request.GET.get("search"):
            search=self.request.GET.get("search")
            queryset=queryset.filter(order_detail__sku__icontains=search)|queryset.filter(order_id__contains=search)\
                |queryset.filter(order_detail__date__icontains=search)\
                |queryset.filter(order_detail__shipping_name__icontains=search)\
                    |queryset.filter(order_detail__shipping_address__icontains=search)\
                        |queryset.filter(order_detail__shipping_city__icontains=search)\
                            |queryset.filter(order_detail__shipping_cap__icontains=search)\
                                |queryset.filter(order_detail__shipping_country__icontains=search)
            
        return queryset.order_by("-order_detail__date").distinct()

class OrderViewSet(OrderViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Order
    permission_class = IsAuthenticated
    serializer_class = OrderSerializer

class OrderDetailViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset("orders")
        return queryset.order_by("id")

class OrderDetailViewSet(OrderDetailViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = OrderDetail
    permission_class = IsAuthenticated
    serializer_class = OrderDetailSerializer


order_list = OrderViewSet.as_view({'get':'list','post':'create'})
order_detail = OrderViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

order_detail_list= OrderDetailViewSet.as_view({'get':'list','post':'create'})
order_detail_detail = OrderDetailViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})


