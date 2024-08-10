from django.db import models


class User(models.Model):
    email = models.EmailField(default="email", unique=True)
    firstname = models.CharField(max_length=20, default="firstname")
    lastname = models.CharField(max_length=20, default="lastname")
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.username

class Feedback(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    message = models.TextField()