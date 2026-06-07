from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    PLAN_CHOICES = [
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        db_column='user_id'
    )
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    company = models.CharField(max_length=200, null=True, blank=True)
    avatar_url = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_profile'
        managed = False

    def __str__(self):
        return f"{self.user.username} — {self.plan}"

    def max_projects(self):
        return {'free': 3, 'pro': 20, 'enterprise': 999}.get(self.plan, 3)

    def max_virtual_users(self):
        return {'free': 50, 'pro': 500, 'enterprise': 5000}.get(self.plan, 50)
