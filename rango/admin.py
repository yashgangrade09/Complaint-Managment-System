from django.contrib import admin
from rango.models import status,office_staff,offices,comp_type, Complaint,village,taluka

# Register your models here.

admin.site.register(Complaint)
admin.site.register(status)
admin.site.register(office_staff)
admin.site.register(offices)
admin.site.register(comp_type)
admin.site.register(taluka)
admin.site.register(village)