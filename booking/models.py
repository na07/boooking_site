from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models

User = get_user_model()

# Create your models here.
class Location(models.Model):
    title = models.CharField(max_length=100,
                             unique=True,
                             validators=[MinLengthValidator(5, message="минимум 5 букв")])
    cost = models.DecimalField(max_digits=7,
                               decimal_places=2,
                               validators=[MinValueValidator(1, message="минимум 1")])
    capacity = models.PositiveIntegerField()
    description = models.TextField()
    def __str__(self):
        return self.title

class Booking(models.Model):
    location = models.ForeignKey(Location,
                                 related_name="bookings",
                                 on_delete=models.CASCADE,
                                 validators=[MinLengthValidator(3, message="минимум 3")])
    user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_field = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.start_date)