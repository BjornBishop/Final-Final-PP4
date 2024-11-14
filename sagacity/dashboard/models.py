
from django.db import models
from django.contrib.auth.models import User
from sagacity.dashboard.models import Assignment, ContactMessage

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

    RATE_PERIOD_CHOICES = [
        ('H', '/Hour'),
        ('D', '/Day'),
        ('M', '/Month'),
    ]

    DURATION_UNIT_CHOICES = [
        ('D', 'Days'),
        ('M', 'Months'),
    ]

    title = models.CharField(max_length=200)
    industry = models.CharField(max_length=3, choices=INDUSTRY_CHOICES)
    duration = models.IntegerField()
    duration_unit = models.CharField(max_length=1, choices=DURATION_UNIT_CHOICES, default='D')
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    rate_period = models.CharField(max_length=1, choices=RATE_PERIOD_CHOICES, default='D')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR')
    requirements = models.TextField(help_text="Separate requirements with '/'")
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_requirements_list(self):
        """Return requirements as a clean list"""
        if not self.requirements:
            return []
        return [req.strip() for req in self.requirements.split('/') if req.strip()]

    def get_duration_display(self):
        """Return formatted duration"""
        unit = 'months' if self.duration_unit == 'M' else 'days'
        return f"{self.duration} {unit}"

    def get_rate_display(self):
        """Return formatted rate"""
        return f"{self.rate} {self.currency}{self.get_rate_period_display()}"

    class Meta:
        app_label = 'sagacity_dashboard'
        ordering = ['-created_at'] # This should make sure the newest assignment appears first 

# Contact form goes here

class ContactMessage(models.Model):
    class Meta:
        app_label = 'sagacity_dashboard'
    from_user = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} regarding {self.assignment.title}"