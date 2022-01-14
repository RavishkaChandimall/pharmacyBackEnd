from rest_framework import serializers

from service.models import UserDetail, Pharmacist, City, Category, Store, Item, ItemStoreWise, Order, OrderDetal, \
    Tester, File, PrescriptionModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = ('id', 'username', 'password', 'name', 'birthday', 'weight', 'lastLoginDate', 'status')


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields = ("id", "username", "password", "name", "pharmacy", "lastLoginDate", "status")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'description')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'description')


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('id', 'name', 'address1', 'address2', 'city', 'contact', 'pharmacy_code')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'description', 'category', 'name')


class ItemStorewiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemStoreWise
        fields = ('id', 'store_id', 'item_id', 'unit_price', 'discount', 'quantity', 'image', 'dosage', "dose_interval")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'date_time', 'customer_id', 'address1', 'address2', 'city', 'status', 'store_id', 'contact')


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetal
        fields = ('id', 'order_id', 'item_id', 'price', 'discount', 'quantity', 'total', 'remark', 'availability')


class TesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tester
        fields = ('id', 'name', 'address1', 'address2', 'city', 'contact', 'pharmacy_code')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'file', 'remark', 'timestamp')


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionModel
        fields = ('id', 'order_id', 'item', 'file_id', 'availability', 'remark')
