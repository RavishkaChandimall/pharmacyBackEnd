from django.contrib import admin

# Register your models here.
from service.models import UserDetail, Pharmacist, City, Category, Store, Item, ItemStoreWise, Order, OrderDetal, \
    Tester, File, PrescriptionModel

admin.site.register(City)
admin.site.register(Category)
admin.site.register(Store)
admin.site.register(Item)
admin.site.register(ItemStoreWise)
admin.site.register(UserDetail)
admin.site.register(Order)
admin.site.register(OrderDetal)
admin.site.register(Pharmacist)
admin.site.register(Tester)
admin.site.register(File)
admin.site.register(PrescriptionModel)
