from django.db import models
from authentication.models import User


class Wallet(models.Model):
    userID = models.ForeignKey(User, related_name="wallet", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.FloatField(null=False)


class Transaction(models.Model):
    TrasnID = models.ForeignKey(Wallet, related_name="transactions", on_delete=models.CASCADE)
    made_at = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(null=False)
    trackID = models.CharField(max_length=255, unique=True)
    successful = models.BooleanField(default=False)





