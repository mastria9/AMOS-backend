# from rest_framework.exceptions import APIException,PermissionDenied
# from companies.models import Company
# from django.db.utils import IntegrityError


# class ShippingMixin(object):
#     def get_queryset(self):
#         try:
#             company=Company.objects.filter(id=self.request.GET.get("company"))
#             queryset=self.model.objects.filter(company=company[0]).order_by('id')
#         except:
#             raise APIException(detail="Devi inserire la ditta")
#         if not self.request.user.is_superuser or not self.request.user.is_staff:
#             company=Company.objects.filter(id=self.request.GET.get("id"),vendors=self.request.user)|\
#                 Company.objects.filter(id=self.request.GET.get("id"),staff=self.request.user)|\
#                     Company.objects.filter(id=self.request.GET.get("id"),collaborators=self.request.user)
#             if company.exists():
#                 queryset=self.model.objects.filter(company=company[0]).order_by("id")
#             else:
#                 raise APIException(detail="Ditta errata")
        
        
#         for key in self.request.GET:
#             if key=="company":
#                 continue
#             else:
#                 queryset=queryset.filter(**{key:self.request.GET.get(key)})
#                 queryset=queryset.order_by('create').order_by('sent')

#         return queryset

#     def perform_create(self,serializer):
#         if not self.request.user.is_superuser and not self.request.user.is_staff:
#             company=Company.objects.filter(vendors=self.request.user)|\
#                 Company.objects.filter(staff=self.request.user)|\
#                     Company.objects.filter(collaborators=self.request.user)
#             try:
#                 if serializer.validated_data["company"] not in company.values_list(flat=True):
#                     raise PermissionDenied(detail="Ditta errata")
#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     raise APIException(detail="Errore!")
#             except IntegrityError as exc:
#                 raise PermissionDenied(detail=exc)
#         else:
#             try:
                
#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     raise APIException(detail="Errore!")
#             except IntegrityError:
#                 raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name))
                
#     def perform_update(self,serializer):
#         if not self.request.user.is_superuser and not self.request.user.is_staff:
#             company=Company.objects.filter(vendors=self.request.user)|\
#                 Company.objects.filter(staff=self.request.user)|\
#                     Company.objects.filter(collaborators=self.request.user)
#             try:
#                 if serializer.validated_data["company"] not in company.values_list(flat=True):
#                     raise PermissionDenied(detail="Ditta errata")
#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     raise APIException(detail="Errore!")
#             except IntegrityError as exc:
#                 raise PermissionDenied(detail=exc)
#         else:
#             try:
#                 if serializer.is_valid():
#                     serializer.save()
#                 else:
#                     raise APIException(detail="Errore!")
#             except IntegrityError:
#                 raise PermissionDenied(detail="%s già esistente" % (self.model._meta.verbose_name))


