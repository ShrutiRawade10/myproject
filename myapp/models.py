from django.db import models
from datetime import date, timedelta

# Create your models here.

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_due_soon(self):
        if self.due_date:
            return date.today() <= self.due_date <= date.today() + timedelta(days=3)
        return False

    @property
    def is_overdue(self):
        if self.due_date:
            return date.today() > self.due_date and not self.completed
        return False
