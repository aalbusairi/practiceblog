from django.db import models
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=20)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('posts:detail', kwargs={"post_id": self.id})	
