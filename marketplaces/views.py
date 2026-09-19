from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_condition import Or,And
from backend.permissions import IsSuperUser,IsStaff
from backend.mixins import AuthorizationMixin,NoAuthorizationMixin
from .models import Marketplace
from rest_framework import serializers

class MarketplaceSerializer(serializers.ModelSerializer):
    _code=serializers.CharField(source="get_code_display",read_only=True)
    _country=serializers.CharField(source="get_country_display",read_only=True)
    class Meta:
        model = Marketplace
        fields = '__all__'
        depth=0
        


class MarketplaceViewMixin(object):
    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.order_by("id")
    

class MarketplaceViewSet(MarketplaceViewMixin,NoAuthorizationMixin,viewsets.ModelViewSet):
    model = Marketplace
    permission_class = IsAuthenticated
    serializer_class = MarketplaceSerializer


marketplace_list = MarketplaceViewSet.as_view({'get':'list','post':'create'})
marketplace_detail = MarketplaceViewSet.as_view({'get':'retrieve','put':'partial_update','delete':'destroy'})



# class MarketplaceAdminViewMixin(object):
#     def get_queryset(self):
#         queryset=super().get_queryset("marketplaces")
#         return queryset.order_by("id")

# class MarketplaceAdminViewSet(MarketplaceAdminViewMixin,AuthorizationMixin,viewsets.ModelViewSet):
#     model = Marketplace
#     permission_class = IsAuthenticated
#     serializer_class = MarketplaceSerializer


# marketplace_list = MarketplaceViewSet.as_view({'get':'list','post':'create'})
# marketplace_detail = MarketplaceViewSet.as_view({'get':'retrieve','put':'update','delete':'destroy'})

