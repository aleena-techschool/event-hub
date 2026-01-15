from django.urls import path
from .views import create_event,event_detail,edit_event,delete_event

urlpatterns = [
    path("create-event/", create_event, name="create_event"),
    path("event/<int:id>/", event_detail,name="event_detail"),
    path("edit-event/<int:id>/", edit_event, name="edit_event"),
    path("delete-event/<int:id>/", delete_event,name="delete_event"),
]
