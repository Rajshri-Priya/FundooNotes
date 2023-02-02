from rest_framework import serializers
from Notes.models import Notes, Labels


class LabelsSerializer(serializers.ModelSerializer):
    """
        Labels Serializer : name
    """

    # name = serializers.CharField(min_length=2, max_length=200, required=True)

    class Meta:
        model = Labels
        fields = ['name']


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'user', 'title', 'description', 'isArchive', 'isTrash', 'color', 'image']
