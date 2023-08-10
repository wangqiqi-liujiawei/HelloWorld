from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=200, unique=True)
    valid_to = models.DateTimeField()
    valid_from = models.DateTimeField()
    active = models.BooleanField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self) -> str:
        return self.code
