from django.urls import path
from backend import views

urlpatterns = [
    path("start_record", views.start_record),
    path("stop_record", views.stop_record),
    path("start_camera", views.start_camera),
    path("stop_camera", views.stop_camera),
    path("save_patient", views.save_patient),
    path("show_patient", views.show_patient),
    path("update_patient", views.update_patient),
    path("inquire_patient", views.inquire_patient),
    path("upload_images", views.upload_images),
    path("delete_items", views.delete_items),
    path("disease_kind", views.disease_kind),
]
