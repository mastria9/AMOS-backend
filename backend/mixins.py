from rest_framework.exceptions import APIException,PermissionDenied
from companies.models import Company,Authorization
from django.db.utils import IntegrityError
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class NoAuthorizationMixin(object):
    def get_queryset(self):
        if not Company.objects.filter(pk=self.request.GET.get("company")).exists():
            raise PermissionDenied("Permesso negato")
        return self.model.objects.filter(company=self.request.GET.get("company"))

class AuthorizationMixin(object):

    def get_queryset(self,application):
        if not Company.objects.filter(pk=self.request.GET.get("company")).exists():
            raise PermissionDenied("Permesso negato")
        if self.request.user.is_superuser or self.request.user.is_staff:
            if "company" in [field.name for field in self.model._meta.fields]:
                return self.model.objects.filter(company=self.request.GET.get("company"))
            else:
                return self.model.objects.all()
        permission=Authorization.Permissions.DENY
        if self.request.method in ["GET"]:
            permission=Authorization.Permissions.READ
        elif self.request.method in ["PUT"]:
            permission=Authorization.Permissions.MODIFY
        # Prendi solo le compagnie cui l'utente ha un permesso uguale o superiore a quello dato
        try:
            if Authorization.objects.get(user=self.request.user,application=application,company=self.request.GET.get("company")).permission<permission:
                raise PermissionDenied("Permesso negato")
        except:
            raise PermissionDenied("Permesso negato")
        if "company" in [field.name for field in self.model._meta.fields]:
            return self.model.objects.filter(company=self.request.GET.get("company"))
        else:
            return self.model.objects.all()





