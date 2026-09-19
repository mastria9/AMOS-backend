from rest_framework import serializers
from .models import Company, Authorization
from django.contrib.auth.models import User

class VendorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name')
        read_only_fields = ('id','username','first_name','last_name')
        

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        depth=0
    

class AuthUserSerializer(serializers.ModelSerializer):
    _last_login=serializers.DateTimeField(source="last_login",format="%d-%m-%Y %H:%M:%S")
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','email','last_login','_last_login','is_active','profile')
        read_only_fields = ('id','username','first_name','last_name','email','last_login','is_active','profile')
        depth=1

class AuthorizationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Authorization
        fields = '__all__'
        
        depth=1



class AuthorizationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authorization
        fields = '__all__'
        
        