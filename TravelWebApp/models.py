from datetime import timedelta
from django.utils.timezone import now
from django.db import models

def default_end_date():
    return now() + timedelta(days=7)

class Travel(models.Model):
    TRANSPORT_CHOICES = (
        ('car', 'Car'),
        ('plane', 'Plane'),
        ('other', 'Other'),
    )

    city = models.CharField(max_length=64, null=False, blank=False, default="")
    country = models.CharField(max_length=64, null=False, blank=False, default="")
    start_date = models.DateField(null=False, blank=False, default=now())
    end_date = models.DateField(null=False, blank=False, default=default_end_date())
    number_of_people = models.PositiveSmallIntegerField(null=False, blank=False, default=1)
    type_of_transport = models.CharField(max_length=10, choices=TRANSPORT_CHOICES, null=False, blank=False, default=TRANSPORT_CHOICES[0])
    description = models.CharField(max_length=1000, null=False, blank=False, default="")
    city_picture = models.ImageField(upload_to='city_images', null=True, blank=True)

    def __str__(self):
        return "{} - {} - {}".format(self.city, self.start_date, self.type_of_transport)


    # Funkcja obliczająca ilość dni to rozpoczęcia podróży
    @property
    def days_to_go(self):
        if (self.start_date - now().date()).days <= 0 and (self.end_date - now().date()).days >= 0:
            return ('In Travel')
        elif (self.start_date - now().date()).days < 0 and (self.end_date - now().date()).days < 0:
            return ('Expired')
        else:
            return (self.start_date - now().date()).days


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, null=True, blank=True, default="")
    completed = models.BooleanField(default=False)
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, default=False, null=False, blank=False)

    def __str__(self):
        return self.title