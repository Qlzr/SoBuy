from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	nickname = models.CharField(max_length=50, blank=True)

	class Meta(AbstractUser.Meta):
		pass

class Collention(models.Model):
	user = models.CharField(max_length=50)
	name = models.CharField(max_length=200)
	price = models.CharField(max_length=12)
	detail_url = models.CharField(max_length=200)
	img_url = models.CharField(max_length=255)
	website = models.CharField(max_length=16)
	collect_time = models.DateTimeField()