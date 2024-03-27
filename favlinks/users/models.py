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
    
class Categorie(models.Model):
    cate_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cate_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    def __str__(self):
        return self.tag_name

class URL(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    categories = models.ManyToManyField(Categorie, blank=True, related_name='urls')
    tags = models.ManyToManyField(Tag, blank=True, related_name='urls')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    create_dtm = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} : {self.url} {self.create_dtm}"