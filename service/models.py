from django.db import models

# Create your models here.
from django.db.models.functions import datetime


class City(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, null=False)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100, null=False)


class Store(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    contact = models.IntegerField(default=0)
    pharmacy_code = models.CharField(max_length=100, null=False)


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, models.CASCADE)
    name = models.CharField(max_length=255)


class ItemStoreWise(models.Model):
    id = models.AutoField(primary_key=True)
    store_id = models.ForeignKey(Store, models.CASCADE)
    item_id = models.ForeignKey(Item, models.CASCADE)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.FileField(blank=False, null=False)
    dosage = models.DecimalField(max_digits=5, decimal_places=2)
    dose_interval = models.DecimalField(max_digits=5, decimal_places=2)


class UserDetail(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    weight = models.IntegerField(default=0)
    lastLoginDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField(null=True)
    customer_id = models.ForeignKey(UserDetail, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    status = models.CharField(max_length=1)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    contact = models.IntegerField(default=0)


class OrderDetal(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_id = models.ForeignKey(ItemStoreWise, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    remark = models.CharField(max_length=1000, null=True)
    availability = models.CharField(max_length=1)


class Pharmacist(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    pharmacy = models.ForeignKey(Store, on_delete=models.CASCADE)
    lastLoginDate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1)


class Tester(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    contact = models.IntegerField
    pharmacy_code = models.CharField(max_length=100, null=False)


class File(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)


class PrescriptionModel(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    file_id = models.ForeignKey(File, on_delete=models.CASCADE)
    availability = models.CharField(max_length=1)
    remark = models.CharField(max_length=255, null=True)
