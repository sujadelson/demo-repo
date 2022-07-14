from django.shortcuts import render
from django.views.generic import TemplateView,CreateView,ListView,DetailView,UpdateView
from bus.forms import BusForm,BusCategoryForm
from bus.models import BusModel

# Create your views here.

class AdminHomeView(TemplateView):
	template_name="adhome.html"

class StaffHomeView(TemplateView):
	template_name="staffhome.html"

class CustomerHomeView(TemplateView):
	template_name="home.html"

class AddBusView(CreateView):
	template_name="addbus.html"
	form_class=BusForm
	success_url="/admin/home/"

class BusListView(ListView):
	template_name='buslist.html'
	model=BusModel
	context_object_name='buslist'

class BusDetailView(DetailView):
	template_name='busdetail.html'
	model=BusModel

class BusEditView(UpdateView):
    model = BusModel
    fields = ['bus_code','source','departure_date',
    'departure_time','destination','arrival_date',
    'arrival_time','bus_type','no_of_seat','remaining_seat','minimum_price']
    template_name='editbus.html'
    success_url='/bus/list/'

class AddBusTypeView(CreateView):
	template_name="addbuscat.html"
	form_class=BusCategoryForm
	success_url="/admin/home/"

class BusListCustView(ListView):
	template_name='buslistcust.html'
	model=BusModel
	context_object_name='buslist'





	