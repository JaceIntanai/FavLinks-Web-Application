from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    e_mail = models.CharField(max_length=40)
    create_dtm = models.DateTimeField(default=timezone.now)

    def __str__(self) :
        return f"{self.username} : {self.first_name} {self.last_name} {self.e_mail} {self.create_dtm}"