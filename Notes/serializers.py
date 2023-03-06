from rest_framework import serializers
from Notes.models import Notes, Labels
from user_auth.models import CustomUser


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
        collaborator_data = self.initial_data.get('collaborator', [])
        collaborators = [get_collaborator(data) for data in collaborator_data]
        collaborators = [collaborator for collaborator in collaborators if collaborator is not None]

        label_name = self.initial_data.get('label')
        notes = Notes.objects.create(**validated_data)
        label = Labels.objects.filter(name=label_name)

        if collaborators:
            notes.collaborator.add(*collaborators)

        if label.exists():
            notes.label.add(label.first())
            return notes

        label = Labels.objects.create(name=label_name, user=validated_data.get("user"))
        notes.label.add(label)
        return notes


def get_collaborator(self, collaborator_data):
    if collaborator_data.isdigit():  # If input is user_id
        return CustomUser.objects.filter(id=collaborator_data).first()
    elif '@' in collaborator_data:  # If input is email
        return CustomUser.objects.filter(email=collaborator_data).first()
    else:  # If input is username
        return CustomUser.objects.filter(username=collaborator_data).first()
