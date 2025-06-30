from django.db import models
import uuid

class AnonymousTip(models.Model):
    CATEGORY_CHOICES = [
        ('corruption','Corruption'),
        ('criminal activity','Criminal  Activity'),
        ('drug related','Drug Related'),
        ('fraud','Fraud'),
        ('violence/threats','Violence/  Threats'),
        ('cybercrime','Cybercrime'),
        ('enviromental crime','Enviromental     Crime'),
        ('other','Other')
    ]
    URGENCY_CHOICES = [
        ('low - general information','Low - General Information'),
        ('medium - requires attention','Medium - Require Attention'),
        ('high - urgent action needed','High - Urgent Action Needed'),
        ('critical - immediate danger','Critical - Immediate Danger')
    ]

    access_key = models.UUIDField(default=uuid.uuid4, editable=False,unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    urgency = models.CharField(max_length=50, choices=URGENCY_CHOICES)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    evidence = models.FileField(upload_to='evidence/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} ({self.urgency})"