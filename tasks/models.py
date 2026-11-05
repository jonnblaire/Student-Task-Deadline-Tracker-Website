from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    color = models.CharField(max_length=7, default='#7C3AED')
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.name} - ({self.code})"
class Task(models.Model):
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    TYPE_CHOICES = [
        ('Assignment', 'Assignment'),
        ('Exam', 'Exam'),
        ('Project', 'Project'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    task_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='assignment') 
    priority = models.CharField(max_length=10, choices = PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title