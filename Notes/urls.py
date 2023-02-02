from django.urls import path

from Notes import views

urlpatterns = [
    path('note/', views.NotesAPIView.as_view(), name='Notes'),
]