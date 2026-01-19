from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from events.models import Event
from datetime import date
from django.utils.timezone import now
from datetime import datetime
import re
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def is_valid_email(email):
    return re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email)

def is_valid_phone(phone):
    return re.match(r"^[6-9]\d{9}$", phone)

def home(request):
    event_type = request.GET.get("type")

    events = Event.objects.filter(is_active=True)

    if event_type:
        events = events.filter(event_type=event_type)

    events = events.order_by("date")

    return render(request, "index.html", {
        "events": events,
        "selected_type": event_type
    })

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"].strip()
        password = request.POST["password"]

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "signin.html", {"error": "Invalid email or password"})

    return render(request, "signin.html")



def signup_view(request):
    if request.method == "POST":
        name = request.POST["name"].strip()
        email = request.POST["email"].strip()
        password = request.POST["password"]

        if not name:
            return render(request, "signup.html", {"error": "Name is required"})

        if not is_valid_email(email):
            return render(request, "signup.html", {"error": "Enter a valid email address"})

        if User.objects.filter(username=email).exists():
            return render(request, "signup.html", {"error": "Email already registered"})

        if len(password) < 6:
            return render(request, "signup.html", {"error": "Password must be at least 6 characters"})

        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        return redirect("/login/")

    return render(request, "signup.html")


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/login/")

    events = Event.objects.filter(created_by=request.user,is_active=True)

    today = date.today()

    upcoming_count = events.filter(date__gte=today).count()
    completed_count = events.filter(date__lt=today).count()

    return render(request, "dashboard.html", {
        "events": events,
        "upcoming_count": upcoming_count,
        "completed_count": completed_count,
    })

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/login/")
    if not request.user.is_superuser:
        return redirect("/dashboard/")

    current_time = now()

    events = Event.objects.all().order_by("-date")
    users = User.objects.filter(is_superuser=False)

    # Compute status per event
    for event in events:
        event_datetime = datetime.combine(event.date, event.time)
        if event_datetime >= current_time.replace(tzinfo=None):
            event.status = "Upcoming"
        else:
            event.status = "Completed"

    total_events = events.count()
    upcoming_events = sum(1 for e in events if e.status == "Upcoming")
    completed_events = sum(1 for e in events if e.status == "Completed")
    total_users = users.count()

    user_stats = []
    for user in users:
        count = Event.objects.filter(created_by=user).count()
        user_stats.append({
            "name": user.first_name,
            "email": user.email,
            "count": count,
            "joined": user.date_joined
        })

    return render(request, "admin.html", {
        "events": events,
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "completed_events": completed_events,
        "total_users": total_users,
        "user_stats": user_stats,
    })


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_admin)
def admin_edit_event(request, id):
    event = get_object_or_404(Event, id=id)

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
        return redirect("/admin-dashboard/")

    return render(request, "edit-event.html", {"event": event})


@user_passes_test(is_admin)
def admin_delete_event(request, id):
    event = get_object_or_404(Event, id=id)
    event.is_active = False   # Soft delete
    event.save()
    return redirect("/admin-dashboard/")


def logout_view(request):
    logout(request)
    return redirect("/")
