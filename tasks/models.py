from django.contrib.auth.models import User
from django.db import models

from statuses.models import Status


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authored_tasks'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT
    )
    labels = models.ManyToManyField(
        'labels.Label',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
