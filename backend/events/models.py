from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    EVENT_TYPES = [
        ("Conference", "Conference"),
        ("Workshop", "Workshop"),
        ("Meetup", "Meetup"),
        ("Networking", "Networking"),
        ("Webinar", "Webinar"),
        ("Hackathon", "Hackathon"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    contact = models.CharField(max_length=20)
    image = models.ImageField(upload_to="events/", null=True, blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
