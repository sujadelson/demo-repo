from django.shortcuts import render,redirect
from django.views.generic import View,ListView
from bus.models import BusModel
from django.contrib.auth.models import User
from booking.forms import ReservationForm
from booking.models import BusBookingModel
from bus.models import BusModel
from django.contrib import messages

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.

class BookModel(View):
	template_name="booking.html"
	def get(self,request,pk):

		data=BusModel.objects.get(id=pk)
		cur_user=str(request.user.username)
		bus_booked=data.bus_code
		source_booked=data.source
		d_date=data.departure_date
		d_time=data.departure_time
		dest_booking=data.destination
		a_date=data.arrival_date
		a_time=data.arrival_time
		bus_type_booking=data.bus_type
		seat_form=ReservationForm()
		price=data.minimum_price 

		context={'user':cur_user,
		'bus_booked':bus_booked,
		'source_booked':source_booked,
		'd_date':d_date,
		'd_time':d_time,
		'dest_booking':dest_booking,
		'a_date':a_date,
		'a_time':a_time,
		'bus_type_booking':bus_type_booking,
		'seat_form':seat_form,
		'price':price,
		}
		print(context)
		return render(request,self.template_name,context)

	def post(self,request,pk):

		if request.POST:
			# print(no_seat)
			data=BusModel.objects.get(id=pk)
			user=str(request.user.username)
			no_seat=request.POST.get('no_of_seat')
			print(no_seat)
			print(data.remaining_seat)
			if int(no_seat)<int(data.remaining_seat):
				bus_booked=data.bus_code
				source_booked=data.source
				d_date=data.departure_date
				d_time=data.departure_time
				dest_booking=data.destination
				a_date=data.arrival_date
				a_time=data.arrival_time
				bus_type_booking=data.bus_type
				price=int(no_seat)*int(data.minimum_price)

				BusBookingModel.objects.create(user=user,
					bus=bus_booked,
					source=source_booked,
					departure_date=d_date,
					departure_time=d_time,
					destination=dest_booking,
					arrival_date=a_date,
					arrival_time=a_time,
					bus_type=bus_type_booking,
					no_of_seat=no_seat,
					price=price)
				return redirect('busconfirm')

			else:

				context={
				'msg':"Sorry, Seat requested is not Available"
				}
				return render(request,'error.html',context)
				# return redirect ('buslist')

class BookConfirmedView(View):
	template_name='bookconfirmed.html'
	def get(self,request):
		data=BusBookingModel.objects.last()
		user=request.user.username
		bus=data.bus
		source=data.source
		d_date=data.departure_date
		d_time=data.departure_time
		dest_booking=data.destination
		a_date=data.arrival_date
		a_time=data.arrival_time
		bus_type=data.bus_type
		no_of_seat=data.no_of_seat
		price=data.price 

		context={
		'bus':bus,
		'source':source,
		'd_date':d_date,
		'd_time':d_time,
		'destination':dest_booking,
		'a_date':a_date,
		'a_time':a_time,
		'bus_type':bus_type,
		'no_of_seat':no_of_seat,
		'price':price,
		}
		print(context)
		return render(request,self.template_name,context)
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

class PaymentView(View):
	template_name="payment.html"

	def get(self,request):
		data=BusBookingModel.objects.last()
		amount=int(data.price)*100
		currency = 'INR'
		# amount = 20000  # Rs. 200
 
		# Create a Razorpay Order
		razorpay_order = razorpay_client.order.create(dict(amount=amount,
			currency=currency,payment_capture='0'))
 
		# order id of newly created order.
		razorpay_order_id = razorpay_order['id']
		callback_url = '/paymenthandler/'
 
		# we need to pass these details to frontend.
		context = {'amount_rupee':data.price}
		context['razorpay_order_id'] = razorpay_order_id
		context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
		context['razorpay_amount'] = amount
		context['currency'] = currency
		context['callback_url'] = callback_url
 
		return render(request,self.template_name, context=context)
 
 
# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):
 
	# only accept POST request.
	if request.method == "POST":
		try:
           
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}
 
			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			print(result)
			if result is None:
				# amount = 20000  # Rs. 200
				data=BusBookingModel.objects.last()
				amount=int(data.price)*100
				
				try:
 
					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)
					data=BusBookingModel.objects.last()
					bus_name=data.bus
					chosen_seat=data.no_of_seat
					bus_data=BusModel.objects.get(bus_code=bus_name)
					bus_data.remaining_seat=bus_data.remaining_seat-chosen_seat
					bus_data.save()
					data.payment_status=True
					data.save()
 
					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:
 
					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:
 
				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:
 
			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
		# if other than POST request is made.
		return HttpResponseBadRequest()

class TicketView(View):
	template_name='ticket.html'
	def get(self,request):
		data=BusBookingModel.objects.filter(payment_status=True).last()
		user=request.user
		bus=data.bus
		source=data.source
		d_date=data.departure_date
		d_time=data.departure_time
		dest_booking=data.destination
		a_date=data.arrival_date
		a_time=data.arrival_time
		bus_type=data.bus_type
		no_of_seat=data.no_of_seat
		price=data.price 

		context={
		'bus':bus,
		'source':source,
		'd_date':d_date,
		'd_time':d_time,
		'destination':dest_booking,
		'a_date':a_date,
		'a_time':a_time,
		'bus_type':bus_type,
		'no_of_seat':no_of_seat,
		'price':price,
		}
		print(context)
		return render(request,self.template_name,context)

class BookingHistory(View):
	template_name = "bookinghistory.html"

	def get(self,request):
		cur_user = str(request.user.username)
		print(cur_user)
		fetch_bookings = BusBookingModel.objects.filter(user=cur_user,payment_status=True)
		print(fetch_bookings)
		context = {
			'bookings':fetch_bookings
		}
		return render(request, self.template_name, context)

class AllBookingHistory(ListView):
	template_name = "allbookinghistory.html"
	model=BusBookingModel
	context_object_name='booklist'
	paginate_by = 4





	