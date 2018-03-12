from django.db import models

# Create your models here.
class VideoSign(models.Model):
	name = models.CharField(max_length=140)
	video = models.FileField(null=True)

	def __str__(self):
		return self.name	
