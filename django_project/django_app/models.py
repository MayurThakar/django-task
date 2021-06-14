from django.db import models
# Create your models here.


class Users(models.Model):
    userid = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.userid
