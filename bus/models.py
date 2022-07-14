from django.db import models

# Create your models here.

class BusCategoryModel(models.Model):
    bus_type=models.CharField(max_length=50)
    created_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_type

class BusModel(models.Model):
    bus_code = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    departure_date=models.DateField(null=False,help_text="Please provide the date in MM/DD/YYYY format")
    departure_time=models.TimeField(null=False,help_text="24 Hour Format")
    destination = models.CharField(max_length=30)
    arrival_date=models.DateField(null=False,help_text="Please provide the date in MM/DD/YYYY format")
    arrival_time=models.TimeField(null=False,help_text="24 Hour Format")
    bus_type=models.ForeignKey(BusCategoryModel,on_delete=models.CASCADE)
    no_of_seat = models.DecimalField(decimal_places=0, max_digits=2)
    remaining_seat = models.DecimalField(decimal_places=0, max_digits=2)
    minimum_price = models.DecimalField(decimal_places=2, max_digits=6)
    status=models.BooleanField(default=1)
    created_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bus_code




