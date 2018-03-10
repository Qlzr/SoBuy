from django.db import models

class Keyword(models.Model):
	word = models.CharField(max_length=150)
	user = models.CharField(max_length=50)
	created_time = models.DateTimeField()

class Commodity(models.Model):
	name = models.CharField(max_length=150)
	price = models.CharField(max_length=12)
	detail_url = models.CharField(max_length=150)
	img_url = models.CharField(max_length=150)
	store = models.CharField(max_length=50)
	store_url = models.CharField(max_length=150)
	website = models.CharField(max_length=16)
	keyword = models.CharField(max_length=150)
	search_time = models.DateTimeField()
	sort_type = models.CharField(max_length=20)