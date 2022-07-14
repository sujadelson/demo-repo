from django.db import models

# Create your models here.
class BusBookingModel(models.Model):
    user=models.CharField(max_length=30)
    bus=models.CharField(max_length=30)
    source=models.CharField(max_length=30)
    departure_date=models.DateField(null=False)
    departure_time=models.TimeField(null=False)
    destination=models.CharField(max_length=30)
    arrival_date=models.DateField(null=False)
    arrival_time=models.TimeField(null=False)
    bus_type=models.CharField(max_length=30)
    no_of_seat=models.IntegerField(default=1)
    price=models.DecimalField(decimal_places=2, max_digits=10)
    payment_status=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now=True)

    def __str__(self):
        return (self.user)