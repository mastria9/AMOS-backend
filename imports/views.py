from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import APIException,PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.db.utils import IntegrityError
from rest_framework.response import Response
from backend.mixins import AuthorizationMixin
from .models import Import
from companies.models import Company
from marketplaces.models import Marketplace
from datetime import datetime
import os
from django.conf import settings
import shutil
from django.http import HttpResponse,HttpResponseNotFound
from rest_framework import serializers


class ImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Import
        fields = '__all__'
        read_only_fields = ('company','marketplace','datasheet','create','status','messages')

class ImportMixin(object):
    def get_queryset(self):
        return super().get_queryset('imports').order_by('-create')
        

    

    def perform_create(self,serializer):
        
        try:
            if serializer.is_valid():
                company=Company.objects.get(id=self.request.GET.get("company"))
                serializer.validated_data["company"]=company
                
                path=os.path.join(settings.PRIVATE_DIR,company.vid,"imports","orders")
                relative_path=os.path.join(company.vid,"imports","orders")
                now=datetime.now()
                extension="txt"
                filename=now.strftime("%Y%m%d%H%M%S")+"_import_"+serializer.validated_data["ftype"]+"."+extension
                if not os.path.exists(path):
                    os.makedirs(path,exist_ok=True)
                shutil.move(self.request.FILES["file"].temporary_file_path(), os.path.join(path,filename))
                serializer.validated_data["path"]=os.path.join(relative_path,filename)
                serializer.save()
        except Exception as e:
            raise APIException(detail="Errore durante il processo di importazione"+str(e))
        
    
       
        

  

class ImportFileMixin(object):
    def retrieve(self,request,pk):
        
    
        importObj=Import.objects.get(id=pk,company=Company.objects.get(id=self.request.GET.get("company")))
        if os.path.exists(os.path.join(settings.PRIVATE_DIR,importObj.path)):

            with open(os.path.join(settings.PRIVATE_DIR,importObj.path), 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(os.path.join(settings.PRIVATE_DIR,importObj.path))
                return response
        return HttpResponseNotFound("File non trovato")


class ImportViewSet(ImportMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Import
    permission_class = IsAuthenticated
    serializer_class = ImportSerializer
    parser_classes= (MultiPartParser,)

    
class ImportFileViewSet(ImportFileMixin,AuthorizationMixin,viewsets.ModelViewSet):
    model = Import
    permission_class = IsAuthenticated
    

import_list = ImportViewSet.as_view({'get':'list','post':'create'})
import_detail = ImportViewSet.as_view({'get':'retrieve'})
import_file = ImportFileViewSet.as_view({'get':'retrieve'})