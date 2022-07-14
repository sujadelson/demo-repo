from django.urls import path,re_path
from booking.views import BookModel,BookConfirmedView,PaymentView,TicketView,BookingHistory,AllBookingHistory
from . import views

urlpatterns = [
    re_path(r'^busbook/(?P<pk>\d+)/$',BookModel.as_view(),name ='busbook'),
    path('bus/confirm/', BookConfirmedView.as_view(), name='busconfirm'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('pay/', PaymentView.as_view(), name='pay'),
    path('ticket/', TicketView.as_view(), name='ticket'),
    path('history/', BookingHistory.as_view(), name='hist'),
    path('all/history/', AllBookingHistory.as_view(), name='allhist'),
    ]