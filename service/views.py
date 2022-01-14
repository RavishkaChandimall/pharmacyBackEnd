import datetime
import random
import string

import cv2
import pytesseract
from PIL import Image
from django.http import FileResponse
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from service.cryptography import Cryptography
from service.models import UserDetail, Pharmacist, ItemStoreWise, Store, City, Category, Item, Order, OrderDetal, \
    PrescriptionModel
from service.serializers import UserSerializer, PharmacySerializer, ItemSerializer, ItemStorewiseSerializer, \
    CitySerializer, StoreSerializer, FileSerializer, PrescriptionItemSerializer, OrderSerializer


class TestView(APIView):
    def post(self, request, *args, **kwargs):
        city = request.data.get('city')
        cityCode = 1
        # cityDetail = City.objects.filter(description=city)
        # if cityDetail.exists():
        #     cityCode = cityDetail.__getitem__(0).id
        # else:
        #     cityObj = {
        #         "description": city
        #     }
        #     citySerializer = CitySerializer(data=cityObj)
        #     if citySerializer.is_valid():
        #         citySerializer.save()
        # S = 10
        # ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k=S))
        # print(ran)
        # storeWiseItem = {
        #     "store_id": 1,
        #     "item_id": 6,
        #     "unit_price": request.data.get('unit_price'),
        #     "discount": request.data.get('discount'),
        #     "quantity": request.data.get('quantity'),
        #     "image": request.data.get('file'),
        #     "dosage": request.data.get('dosage'),
        #     "dose_interval": request.data.get('dosage_interval')
        # }
        # storeWiseSerializer = ItemStorewiseSerializer(data=storeWiseItem)
        # if storeWiseSerializer.is_valid():
        #     storeWiseSerializer.save()
        #     success = True
        # testSerializer = TesterSerializer(data=pharmacy)
        # if testSerializer.is_valid():
        #     testSerializer.save()
        object = ItemStoreWise.objects.filter(id=2)

        return Response("SUCCESS", status=status.HTTP_201_CREATED)
        # else:
        #     return Response('FAIL', status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        items = ItemStoreWise.objects.all()
        return FileResponse(items.__getitem__(0).image, status=status.HTTP_200_OK)


class User(APIView):
    def post(self, request, *args, **kwargs):
        cryp = Cryptography()
        password = request.data.get('password')
        encPassword = cryp.encrypt(password)
        user = {
            "username": request.data.get('username'),
            "password": str(encPassword),
            "status": request.data.get('status')
        }
        user_serializer = UserSerializer(data=user)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("SUCCESS", status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Signup(APIView):
    def post(self, request, *args, **kwargs):
        cryp = Cryptography()
        username = request.data.get('username')
        password = request.data.get('password')
        encPassword = cryp.encrypt(password)
        userDetail = UserDetail.objects.filter(username=username)
        if userDetail.exists():
            return Response("USERNAME EXISTS", status=status.HTTP_400_BAD_REQUEST)
        userDetail = Pharmacist.objects.filter(username=username)
        if userDetail.exists():
            return Response("USERNAME EXISTS", status=status.HTTP_400_BAD_REQUEST)
        user = {
            "username": username,
            "password": encPassword,
            "name": request.data.get('name'),
            "birthday": request.data.get('birthday'),
            "weight": request.data.get('weight'),
            "status": request.data.get('status')
        }
        user_serializer = UserSerializer(data=user)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("SUCCESS", status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def create_user(request):
#     if (request.method == 'POST'):

class SignupPharmacy(APIView):
    def post(self, request, *args, **kwargs):
        cryp = Cryptography()
        username = request.data.get('username')
        password = request.data.get('password')
        pharmacyCode = request.data.get('pharmacy-code')
        pharmacyId = 0
        encPassword = cryp.encrypt(password)
        city = request.data.get('city')
        cityDetail = City.objects.filter(description=city)[0:1]
        userDetail = Pharmacist.objects.filter(username=username)[0:1]
        pharmacy = Store.objects.filter(name=pharmacyCode)[0:1]
        pharmacyByCode = Store.objects.filter(pharmacy_code=pharmacyCode)[0:1]
        if userDetail.exists():
            return Response("USERNAME EXISTS", status=status.HTTP_400_BAD_REQUEST)
        userDetail = UserDetail.objects.filter(username=username)
        if userDetail.exists():
            return Response("USERNAME EXISTS", status=status.HTTP_400_BAD_REQUEST)
        if pharmacy.exists():
            return Response("PHARMACY EXISTS, PLEASE REGISTER WITH CODE", status=status.HTTP_400_BAD_REQUEST)
        if pharmacyByCode.exists():
            pharmacyId = pharmacyByCode.__getitem__(0).id
        else:
            count = 10
            pharmacyCode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=count))
            cityCode = 0
            if cityDetail.exists():
                cityCode = cityDetail.__getitem__(0).id
            else:
                cityObj = {
                    "description": city
                }
                citySerializer = CitySerializer(data=cityObj);
                if citySerializer.is_valid():
                    citySerializer.save()
                    cityCode = citySerializer.data.id
            pharmacy = {
                "name": request.data.get('name'),
                "address1": request.data.get('address1'),
                "address2": request.data.get('address2'),
                "city": cityCode,
                "contact": request.data.get('contact'),
                "pharmacy_code": pharmacyCode
            }
            pharmacySerializer = StoreSerializer(data=pharmacy);
            if pharmacySerializer.is_valid():
                pharmacySerializer.save()
                pharmacyId = pharmacySerializer.data.get('id')
        user = {
            "username": username,
            "password": encPassword,
            "name": request.data.get('name'),
            "status": 'A',
            "pharmacy": pharmacyId,
        }
        user_serializer = PharmacySerializer(data=user)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response("SUCCESS", status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        userDetail = UserDetail.objects.filter(username=username)[0:1]
        pharmacistDetail = Pharmacist.objects.filter(username=username)[0:1]
        isValid = False
        user = False
        store = 0
        cryp = Cryptography()
        if userDetail.exists():
            isValid = cryp.validate(password, userDetail.__getitem__(0).password)
            user = True
        elif pharmacistDetail.exists():
            userDetail = pharmacistDetail
            isValid = cryp.validate(password, userDetail.__getitem__(0).password)
            store = userDetail.__getitem__(0).pharmacy.id
        if isValid:
            user = {
                "username": userDetail.__getitem__(0).username,
                "name": userDetail.__getitem__(0).name,
                "password": password,
                "user": user,
                "store": store
            }
            return Response(user, status.HTTP_200_OK)
        else:
            return Response("FAILED", status.HTTP_401_UNAUTHORIZED)


class AddItem(APIView):
    def post(self, request, *args, **kwargs):
        success = False
        storeWiseItemDetail = ItemStoreWise.objects.filter(id=request.data.get('id'))[0:1]
        userDetail = Pharmacist.objects.filter(username=request.data.get('userId'))[0:1]

        storeWiseItem = {}
        if storeWiseItemDetail.exists():
            storeWiseItem = {
                "id": storeWiseItemDetail.__getitem__(0).id,
                "store_id": storeWiseItemDetail.__getitem__(0).storeId,
                "item_id": storeWiseItemDetail.__getitem__(0).itemId,
                "unit_price": request.data.get('unit_price'),
                "discount": request.data.get('discount'),
                "quantity": request.data.get('quantity'),
                "image": request.data.get('file'),
                "dosage": request.data.get('dosage'),
                "dose_interval": request.data.get('dosage_interval')
            }
        else:
            item = {
                "id": 0,
                "description": request.data.get('description'),
                "category": 1,
                "name": request.data.get('name')
            }
            itemSerializer = ItemSerializer(data=item)
            if itemSerializer.is_valid():
                itemSerializer.save()
                storeWiseItem = {
                    "store_id": userDetail.__getitem__(0).pharmacy.id,
                    "item_id": itemSerializer.data.get('id'),
                    "unit_price": request.data.get('unit_price'),
                    "discount": request.data.get('discount'),
                    "quantity": request.data.get('quantity'),
                    "image": request.data.get('file'),
                    "dosage": request.data.get('dosage'),
                    "dose_interval": request.data.get('dosage_interval')
                }
                storeWiseSerializer = ItemStorewiseSerializer(data=storeWiseItem)
                if storeWiseSerializer.is_valid():
                    storeWiseSerializer.save()
                    success = True
        if success:
            return Response(storeWiseItem, status.HTTP_200_OK)
        else:
            return Response("FAILED", status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        items = Item.objects.all()
        itemList = []
        for i in items:
            item = {
                "id": i.id,
                "name": i.name,
                "description": i.description,
                "category": i.category_id
            }
            itemList.append(item)
        list = {
            "list": itemList
        }
        return Response(list, status=status.HTTP_200_OK)


class placeOrder(APIView):
    def post(self, request, *args, **kwargs):
        success = False
        city = request.data.get('city')
        if not city.isnumeric():
            cityModel = {
                'id': 0,
                'description': city
            }
            citySerializer = CitySerializer(data=cityModel)
            if citySerializer.is_valid():
                citySerializer.save()
                city = cityModel.id
        order = {
            'id': request.data.get('id'),
            'date_time': request.data.get('dateTime'),
            'customer_id': request.data.get('customerId'),
            'address1': request.data.get('address1'),
            'address2': request.data.get('address2'),
            'city': city,
            'status': 'A',
            'store_id': request.data.get('storeId'),
            'contact': request.data.get('quantity')
        }
        orderDetails = request.request.data.get('orderDetail')
        for detail in orderDetails:
            orderDetail = {
                'id': detail.id,
                'order_id': detail.orderId,
                'item_id': detail.itemId,
                'price': detail.price,
                'discount': detail.discount,
                'quantity': detail.quantity,
                'total': detail.total,
                'remark': detail.remark,
                'availability': detail.availability,
            }
        if success:
            return Response("SUCCESS", status.HTTP_200_OK)
        else:
            return Response("FAILED", status.HTTP_401_UNAUTHORIZED)

    def get(self, request, *args, **kwargs):
        return Response("SUCCESS", status=status.HTTP_200_OK)


class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        categoryList = []
        for i in categories:
            category = {
                "id": i.id,
                "description": i.description,
            }
            categoryList.append(category)
        list = {
            "list": categoryList
        }
        return Response(list, status=status.HTTP_200_OK)


class ItemStore(APIView):
    def get(self, request, *args, **kwargs):
        storeId = request.query_params.get('store-id')
        if storeId:
            items = ItemStoreWise.objects.filter(store_id=storeId)
        else:
            items = ItemStoreWise.objects.all()
        itemList = []
        for i in items:
            item = {
                "id": i.id,
                "storeId": i.store_id.id,
                "itemId": i.item_id.id,
                "unitPrice": i.unit_price,
                "discount": i.discount,
                "quantity": i.quantity,
                "image": i.image.file.name,
                "dosage": i.dosage,
                "dosageInterval": i.dose_interval
            }
            itemList.append(item)
        list = {
            "list": itemList
        }
        return Response(list, status=status.HTTP_200_OK)


class ItemImage(APIView):
    def get(self, request, *args, **kwargs):
        items = ItemStoreWise.objects.filter(id=request.query_params.get('id'))[0:1]
        return FileResponse(items.__getitem__(0).image, status=status.HTTP_200_OK)


class AllOrders(APIView):
    def get(self, request, *args, **kwargs):
        storeId = request.query_params.get('store-id')
        userId = request.query_params.get('user-id')
        if (storeId != None):
            orders = Order.objects.filter(store_id=storeId)
        else:
            orders = Order.objects.filter(customer_id=userId)
        orderList = []
        for order in orders:
            orderDetails = OrderDetal.objects.filter(order_id=order.id)
            orderDetailList = []
            itemList = []
            if orderDetails.exists():
                for orderDetail in orderDetails:
                    orderDetailObj = {
                        "id": orderDetail.id,
                        "orderId": orderDetail.order_id.id,
                        "itemId": orderDetail.item_id.id,
                        "unitPrice": orderDetail.price,
                        "discount": orderDetail.discount,
                        "quantity": orderDetail.quantity,
                        "total": orderDetail.total,
                        "remark": orderDetail.remark,
                        "availability": orderDetail.availability
                    }
                    orderDetailList.append(orderDetailObj)
            else:
                orderDetails = PrescriptionModel.objects.filter(order_id=order.id)
                for orderDetail in orderDetails:
                    itemList.append(orderDetail.item)

            orderObj = {
                "id": order.id,
                "date": order.date_time,
                "customer": order.customer_id.id,
                "address1": order.address1,
                "address2": order.address2,
                "city": order.city.id,
                "contact": order.contact,
                "status": order.status,
                "store": order.store_id.id,
                "orderDetails": {
                    "list": orderDetailList
                },
                "items": itemList
            }
            orderList.append(orderObj)
        list = {
            "list": orderList
        }
        return Response(list, status=status.HTTP_200_OK)


class UserDetails(APIView):
    def get(self, request, *args, **kwargs):
        users = UserDetail.objects.all()
        userList = []
        for i in users:
            userDetail = {
                "id": i.id,
                "name": i.name,
                "userName": i.username,
                "birthday": i.birthday,
                "weight": i.weight,
                "status": i.status
            }
            userList.append(userDetail)
        list = {
            "list": userList
        }
        return Response(list, status=status.HTTP_200_OK)


class CityDetail(APIView):
    def get(self, request, *args, **kwargs):
        cities = City.objects.all()
        cityList = []
        for city in cities:
            cityObj = {
                "id": city.id,
                "description": city.description
            }
            cityList.append(cityObj)
        list = {
            "list": cityList
        }
        return Response(list, status=status.HTTP_200_OK)


class StoreDetails(APIView):
    def get(self, request, *args, **kwargs):
        stores = Store.objects.all()
        storeList = []
        for store in stores:
            storeObj = {
                "id": store.id,
                "name": store.name,
                "address1": store.address1,
                "address2": store.address2,
                "city": store.city.id,
                "contact": store.contact
            }
            storeList.append(storeObj)
        list = {
            "list": storeList
        }
        return Response(list, status=status.HTTP_200_OK)


class FileUpload(APIView):
  parser_classes = (MultiPartParser, FormParser)

  def post(self, request, *args, **kwargs):
    file_serializer = FileSerializer(data=request.data)
    if file_serializer.is_valid():
      file_serializer.save()

      image_to_ocr = cv2.imread(file_serializer.data.get('file').replace('/', '', 1))
      preprocessed_image = cv2.cvtColor(image_to_ocr, cv2.COLOR_BGR2GRAY)
      preprocessed_image = cv2.threshold(preprocessed_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
      # cv2.imshow("Actual Image", preprocessed_image)
      # cv2.waitKey()
      preprocessed_image = cv2.medianBlur(preprocessed_image, 3)

      cv2.imwrite('temp_img.jpg', preprocessed_image)

      preprocessed_pil_img = Image.open('temp_img.jpg')
      text_extracted = pytesseract.image_to_string(preprocessed_pil_img)
      print(text_extracted)
      city = {
          "description": request.data.get('city')
      }
      cityId=0
      cityDetail = City.objects.filter(description=request.data.get('city'))[0:1]
      if cityDetail.exists():
          cityId = cityDetail.__getitem__(0).id
      else:
          citySerializer = CitySerializer(data=city)
          if citySerializer.is_valid():
              citySerializer.save()
              cityId = citySerializer.data.get('id'),
      userDetail = UserDetail.objects.filter(username=request.data.get('user-name'))[0:1]
      order = {
          "date_time": datetime.datetime.now(),
          "customer_id": userDetail.__getitem__(0).id,
          "address1": request.data.get('address1'),
          "address2": request.data.get('address2'),
          "city": cityId,
          "status": 'P',
          "store_id": request.data.get('store-id'),
          "contact": request.data.get('contact'),
      }
      orderSerializer = OrderSerializer(data=order)
      if orderSerializer.is_valid():
          orderSerializer.save()
      for text in text_extracted.rsplit('\n'):
          obj = {
              "order_id": orderSerializer.data.get('id'),
              "item": text,
              "file_id": file_serializer.data.get('id'),
              "availability": "A",
              "remark": "A"
          }
          prescriptionSerializer = PrescriptionItemSerializer(data=obj)
          if prescriptionSerializer.is_valid():
              prescriptionSerializer.save()
      cv2.waitKey()

      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrescriptionImage(APIView):
    def get(self, request, *args, **kwargs):
        prescription = PrescriptionModel.objects.filter(order_id=request.query_params.get('order-id'))[0:1]
        return FileResponse(prescription.__getitem__(0).file_id.file, status=status.HTTP_200_OK)
