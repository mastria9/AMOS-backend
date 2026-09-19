from django.contrib import admin
from .models import Company,Authorization






class CompanyAdmin(admin.ModelAdmin):
    list_display =  ('pk','vid','name','vat','city','province','country','pec','sdi','created_at','updated_at','active')
    search_fields = ('vid','name','vat','city','sdi')


class AuthorizationAdmin(admin.ModelAdmin):
    list_display =  ('pk','company','user','application','permission')



admin.site.register(Company,CompanyAdmin)

admin.site.register(Authorization,AuthorizationAdmin)