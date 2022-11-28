from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils import timezone
from cart.models import Course



class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    courses = models.ManyToManyField(Course)
    pub_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, unique_for_date="pub_date")

    def get_absolute_url(self):
        return reverse("schedule:schedule_view", args=[self.slug])

    class Meta:
        ordering = ("pub_date",)


class Comment(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=25) 
    content = models.TextField(max_length=250)
    pub_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "comments"
        ordering = ('pub_date',)

    def __str__(self):
        return f"Comment by {self.name}"


# Create your models here.
