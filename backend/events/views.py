from django.shortcuts import render, redirect,get_object_or_404
from .models import Event
from datetime import datetime
import re

def is_valid_phone(phone):
    return re.match(r"^[6-9]\d{9}$", phone)

def create_event(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    if request.method == "POST":
        title = request.POST["title"].strip()
        description = request.POST["description"].strip()
        date = request.POST["date"]
        time = request.POST["time"]
        location = request.POST["location"].strip()
        event_type = request.POST["type"]
        contact = request.POST["contact"].strip()

        if not title or not description or not location:
            return render(request, "create-event.html", {"error": "All fields are required"})

        if not is_valid_phone(contact):
            return render(request, "create-event.html", {"error": "Enter valid phone number"})

        event_date_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        if event_date_time < datetime.now():
            return render(request, "create-event.html", {"error": "Event date cannot be in the past"})

        Event.objects.create(
            title=title,
            description=description,
            date=date,
            time=time,
            location=location,
            event_type=event_type,
            contact=contact,
            image=request.FILES.get("image"),
            created_by=request.user
        )

        if request.user.is_superuser:
            return redirect("/admin-dashboard/")
        else:
            return redirect("/dashboard/")

    return render(request, "create-event.html")


def edit_event(request, id):
    if not request.user.is_authenticated:
        return redirect("/login/")

    event = get_object_or_404(Event, id=id, created_by=request.user)

    if request.method == "POST":
        event.title = request.POST["title"]
        event.description = request.POST["description"]
        event.date = request.POST["date"]
        event.time = request.POST["time"]
        event.location = request.POST["location"]
        event.event_type = request.POST["type"]
        event.contact = request.POST["contact"]

        if request.FILES.get("image"):
            event.image = request.FILES.get("image")

        event.save()
        return redirect("/dashboard/")

    return render(request, "edit-event.html", {"event": event})


def delete_event(request, id):
    event = get_object_or_404(Event, id=id, created_by=request.user)
    event.is_active = False
    event.save()
    return redirect("/dashboard/")


def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    return render(request, "event-details.html", {"event": event})