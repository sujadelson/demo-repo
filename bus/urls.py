from django.urls import path,re_path
from bus.views import CustomerHomeView,StaffHomeView,AdminHomeView,BusListCustView,AddBusView,BusListView,BusDetailView,BusEditView,AddBusTypeView

urlpatterns = [
    path('', CustomerHomeView.as_view(), name='chome'),
    path('staff/home/', StaffHomeView.as_view(), name='shome'),
    path('admin/home/', AdminHomeView.as_view(), name='ahome'),
    path('add/bus/', AddBusView.as_view(), name='addbus'),
    path('bus/list/',BusListView.as_view(),name = 'buslist'),
    re_path(r'^busdetail/(?P<pk>\d+)/$',BusDetailView.as_view(),name ='busdetail'),
    re_path(r'^busedit/(?P<pk>\d+)/$',BusEditView.as_view(),name ='busedit'),
    path('add/bus/category/', AddBusTypeView.as_view(), name='addbuscat'),
    path('list/', BusListCustView.as_view(), name='cbuslist'),
    ]

    