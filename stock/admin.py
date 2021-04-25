from django.contrib import admin
# Register your models here.
from stock.models import Stock, Mystock,Condition_Sheet
admin.site.register(Stock)
admin.site.register(Mystock)
admin.site.register(Condition_Sheet)