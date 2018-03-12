from django.db import models

class Keyword(models.Model):
	word = models.CharField(max_length=150)
	user = models.CharField(max_length=50)
	created_time = models.DateTimeField()