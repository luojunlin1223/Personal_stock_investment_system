from django.contrib import admin

# Register your models here.
from stock.models import Stock, Mystock
class StockAdmin(admin.ModelAdmin):
    list_display =('code','name')
class MyStockAdmin(admin.ModelAdmin):
    list_display = ('user','stock','created_on')
admin.site.register(Stock)
admin.site.register(Mystock)