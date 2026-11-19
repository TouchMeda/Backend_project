from django.conf import settings
from django.db import models



class Tag(models.Model):
	
	name = models.CharField(max_length=50, unique=True)
	
	
	class Meta:
		ordering = ["name"]

	def __str__(self):
		return self.name



class Server(models.Model):
	class Status(models.TextChoices):
		ACTIVE = "active"
		MAINTENANCE = "maintenance"
		DECOMMISSIONED = "decommissioned"
		
	hostname = models.CharField(max_length=255, unique=True)
	ip_address = models.GenericIPAddressField()
	os = models.CharField(max_length=100, blank=True)
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="servers"
	)
	
	status = models.CharField(
		max_length=20, choices=Status.choices, default=Status.ACTIVE	
	)
	
	tags = models.ManyToManyField(Tag, related_name="servers", blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	
	
	class Meta:
		ordering = ["hostname"]
		indexes = [
			models.Index(fields=["status", "hostname"])
		]
	
	def __str__(self):
		return f"{self.hostname} ({self.ip_address})"
