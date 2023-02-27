from rest_framework import serializers
from Notes.models import Notes, Labels
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['name']
        extra_kwargs = {'user': {'required': True}}


class NotesSerializer(serializers.ModelSerializer):
    label = LabelsSerializer(many=True, read_only=True)

    class Meta:
        model = Notes
        fields = ['id', 'user', 'title', 'description', 'isArchive', 'isTrash', 'color', 'image', 'label',
                  'collaborator', 'reminder']
        read_only_fields = ['label', 'collaborator']

    def create(self, validated_data):
        label_name = self.initial_data.get('label')
        notes = Notes.objects.create(**validated_data)
        label = Labels.objects.filter(name=label_name)

        if label.exists():
            notes.label.add(label.first())
            return notes

        label = Labels.objects.create(name=label_name, user=validated_data.get("user"))
        notes.label.add(label)
        return notes


