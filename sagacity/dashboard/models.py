
from django.db import models
from django.contrib.auth.models import User

# Models go below here

class Assignment(models.Model):
    INDUSTRY_CHOICES = [
        ('FS', 'Financial Services'),
        ('COM', 'Commercial'),
        ('IND', 'Industrial'),
    ]
    
    CURRENCY_CHOICES = [
        ('EUR', 'Euro'),
        ('SEK', 'Swedish Krona'),
    ]

    title = models.CharField(max_length=200)
    industry = models.CharField(max_length=3, choices=INDUSTRY_CHOICES)
    duration = models.IntegerField(help_text="Duration in days")
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR')
    requirements = models.TextField(help_text="Separate requirements with '/'")
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return a string representation of the assignment"""
        return self.title

    class Meta:
        ordering = ['-created_at']  # Newest assignments first