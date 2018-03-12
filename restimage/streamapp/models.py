from django.db import models

# Create your models here.
class VideoStream(models.Model):
	video = models.FileField(null=True)

	def __str__(self):
		return self.name	

