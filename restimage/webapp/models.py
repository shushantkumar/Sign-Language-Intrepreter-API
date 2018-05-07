from django.db import models

# Create your models here.
class Stock(models.Model):
	name = models.CharField(max_length=140)
	image = models.FileField(null=True)

	def __str__(self):
		return self.name	

