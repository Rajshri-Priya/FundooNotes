from django.urls import path

from Notes import views
from Notes.views import NotesCollaboratorAPIView

urlpatterns = [
    path('note', views.NotesAPIView.as_view(), name='notes'),
    path('note/<int:note_id>/', views.NotesAPIView.as_view(), name='note_id'),
    path('label', views.LabelsAPIView.as_view(), name='label'),
    path('label/<str:label_name>/', views.LabelsAPIView.as_view(), name='label_name'),
    path('archive', views.ArchiveNoteList.as_view(), name='archive'),
    path('archive/<int:note_id>/', views.ArchiveNoteList.as_view(), name='archive-update'),
    path('trash', views.TrashNotesAPIView.as_view(), name='trash'),
    path('trash/<int:note_id>/', views.TrashNotesAPIView.as_view(), name='trash-update'),
    path('collaborator/<int:note_id>/', NotesCollaboratorAPIView.as_view(), name='notes-collaborators'),
    path('collaborator/<int:note_id>/<int:user_id>/', NotesCollaboratorAPIView.as_view(),
         name='notes-collaborator'),
    # path('notes/<int:note_id>/collaborators/<int:user_id>/', NotesCollaboratorAPIView.as_view()),

]