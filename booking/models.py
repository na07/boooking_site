from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
                                 on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    activation_token = models.CharField(max_length=16, null=True, blank=True)


    def __str__(self):
        return str(self.start_date) + self.user.username

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError(_("Дата начала должна быть раньше даты окончания."))

        if Booking.objects.filter(
            (models.Q(start_date__lte=self.end_date) & models.Q(end_date__gte=self.start_date))
        ).exclude(pk=self.pk).exists():
            raise ValidationError(_("Этот период уже забронирован."))

    def save(self, *args, **kwargs):
        self.clean()  # Вызываем проверку перед сохранением
        super().save(*args, **kwargs)
