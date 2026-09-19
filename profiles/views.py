from pprint import PrettyPrinter
from rest_framework.exceptions import APIException,PermissionDenied
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from companies.models import Company
from profiles.models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User
from django.http.response import JsonResponse
import json
from django.core.mail import send_mail

class UserSerializer(serializers.ModelSerializer):
    _last_login=serializers.DateTimeField(source="last_login",format="%d-%m-%Y %H:%M:%S")
    _date_joined=serializers.DateTimeField(source="date_joined",format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = User
        fields = ('id','_last_login','last_login','is_superuser','username',"first_name","last_name","email","is_staff","is_active","date_joined","_date_joined","profile")
        read_only_fields = ('_last_login','last_login','is_superuser','username',"is_staff","is_active","date_joined","_date_joined","profile")
        depth=1


        


class UserFilterMixin(object):
    def get_queryset(self):
        #se superuser ... tutti
        #se staff tutti
        queryset=User.objects.all().order_by("last_name")
        return queryset

    def perform_create(self,serializer):
        if serializer.is_valid():
            user=User(username=serializer.validated_data["email"])
            user.first_name=serializer.validated_data["first_name"]
            user.last_name=serializer.validated_data["last_name"]
            user.email=serializer.validated_data["email"]
            user.is_active=False
            try:
                user.save()
            except Exception:
                raise APIException(detail="Errore nel creare un nuovo utente!")    
            password=User.objects.make_random_password()
            user.set_password(password)
            user.save()
            send_mail('Benvenuto in Nevix.Cloud Venditori','Puoi accedere utilizzando il tuo username e la password '+password,'info@nevix.cloud',['info@nevix.cloud',user.email],fail_silently=True,)
        else:
            raise APIException(detail="Errore! Dati non validi")

    def perform_update(self,serializer):
        if serializer.is_valid():
            serializer.save()
            if "profile" in serializer.initial_data and "phone" in serializer.initial_data["profile"]:
                user=User.objects.get(id=serializer.data["id"])
                if Profile.objects.filter(user=user).exists():
                    profile=Profile.objects.get(user=user)
                    profile.phone=serializer.initial_data["profile"]["phone"]
                    profile.save()
                else:
                    profile=Profile(user=user,phone=serializer.initial_data["profile"]["phone"])
                    profile.save()

        


class UserViewSet(UserFilterMixin,viewsets.ModelViewSet):
    model = User
    permission_class = IsAuthenticated
    serializer_class = UserSerializer



class UserMeMixin(object):
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id).order_by("id")


        
class UserMeViewSet(UserMeMixin,viewsets.ModelViewSet):
    model = User
    permission_class = IsAuthenticated
    serializer_class = UserSerializer


user_list = UserViewSet.as_view({'get':'list','post':'create'})
user_detail = UserViewSet.as_view({'get':'retrieve','put':'partial_update',})
user_me_detail = UserMeViewSet.as_view({'get':'list'})