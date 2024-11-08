from django.db import models

# Create your models here.
# challenges/models.py
from django.db import models
from django.contrib.auth.models import User


class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problems_solved = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"
    from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    tags = models.CharField(max_length=100)
    test_cases = models.JSONField()  # Store each test case as {"input": "input_str", "output": "expected_output"}

    def __str__(self):
        return self.title

class Submission(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('R', 'Running'),
        ('C', 'Completed'),
        ('E', 'Error')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    result = models.JSONField(default=dict)  # Store detailed results per test case and overall score
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Problem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    tags = models.CharField(max_length=100)
    test_cases = models.JSONField()

    def __str__(self):
        return self.title

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=50)
    result = models.TextField()
    status = models.CharField(max_length=1, choices=[('P', 'Pending'), ('C', 'Completed'), ('E', 'Error')], default='P')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"

class Leaderboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problems_solved = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"

from django.db import models
from django.contrib.auth.models import User



