from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileSerializer
from PIL import Image
import pytesseract
import cv2

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
      cv2.waitKey()

      return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
      return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class FileView(APIView):
#   def get(self, request, *args, **kwargs):
