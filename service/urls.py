from django.conf.urls import url
from .views import TestView, User, Signup, Login, SignupPharmacy, AddItem, CategoryView, ItemStore, ItemImage, \
    AllOrders, UserDetails, CityDetail, StoreDetails, FileUpload, PrescriptionImage

urlpatterns = [
    url(r'^test/$', TestView.as_view(), name='test-api'),
    url(r'^user/$', User.as_view(), name='user-api'),
    url(r'^signup/$', Signup.as_view(), name='user-api'),
    url(r'^login/$', Login.as_view(), name='user-api'),
    url(r'^pharmacy-signup/$', SignupPharmacy.as_view(), name='user-api'),
    url(r'^new-item/$', AddItem.as_view(), name='user-api'),
    url(r'^category/$', CategoryView.as_view(), name='user-api'),
    url(r'^item-store/$', ItemStore.as_view(), name='user-api'),
    url(r'^item-image/$', ItemImage.as_view(), name='user-api'),
    url(r'^orders/$', AllOrders.as_view(), name='user-api'),
    url(r'^user-detail/$', UserDetails.as_view(), name='user-api'),
    url(r'^city-detail/$', CityDetail.as_view(), name='user-api'),
    url(r'^store-detail/$', StoreDetails.as_view(), name='user-api'),
    url(r'^upload/$', FileUpload.as_view(), name='user-api'),
    url(r'^prescription-image/$', PrescriptionImage.as_view(), name='user-api')
]
