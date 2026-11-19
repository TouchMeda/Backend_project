from django.conf import settings
from django.db import models
from django.db.models import Q

from inventory.models import Server



class Incident(models.Model):
	class Severity(models.TextChoices):
		LOW = "low"
		MDIUM = "medium"
		HIGH = "high"
		CRITICAL = "critical"
		
	class Status(models.TextChoices):
		OPEN = "open"
		IN_PROGRESS = "in_progress"
		RESOLVED = "resolved"
		
	server = models.ForeignKey(
		Server, on_delete=models.CASCADE, related_name="incidents"
	)
	
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	severity = models.CharField(
		max_length=20, choices=Status.choices, default=Status.OPEN
	)
	
	status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OPEN
    )
	
	assignee = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name="assigned_incidents"
	)
	
	created_at = models.DateTimeField(auto_now_add=True)
	resolved_at = models.DateTimeField(null=True, blank=True)
	
	
	class Meta:
		ordering = ["-created_at"]
		indexes = [
			models.Index(fields=["status", "severity"]),
			models.Index(fields=["server", "-created_at"])
		]
		constraints = [
		models.CheckConstraint(
			condition=~Q(status="resolved") | Q(resolved_at__isnull=False),
			name="resolved_requires_resolved_at"
			)
		]
	
	def __str__(self):
		return f"[{self.get_severity_display()}] {self.title}"
		
		
class IncidentComment(models.Model):
	incident = models.ForeignKey(
		Incident, on_delete=models.CASCADE, related_name="comments"
	)
	
	author = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.PROTECT,
		related_name="incident_comments"
	)
	
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	
	
	class Meta:
		ordering = ["created_at"]
		
	def __str__(self):
		return f"Comment {self.author} to {self.incident}"
