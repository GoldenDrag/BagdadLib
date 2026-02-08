from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("latest/", views.latest, name="latest"),
    path("<int:book_id>/", views.detail, name="detail"),
    path("<int:chapter_id>/", views.read, name="read"),
    path("upload/", views.upload_book, name="upload")
]