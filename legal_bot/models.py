from django.db import models
from django.utils import timezone

# Create your models here.


class ChatHistory(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Q: {self.question[:50]}..."


class ScoringHistory(models.Model):
    query = models.TextField()
    response_1 = models.TextField()
    response_2 = models.TextField()
    response_3 = models.TextField()
    scoring_result = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Scoring for query: {self.query[:50]}..."
