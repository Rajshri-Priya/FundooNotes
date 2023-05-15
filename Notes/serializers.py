from rest_framework import serializers
from Notes.models import Notes, Labels
from user_auth.models import CustomUser
from logging_confiq.logger import get_logger

# logger config
logger = get_logger()


def get_collaborator(self, collaborator_data):
    try:
        if isinstance(collaborator_data, int):  # Check if collaborator_data is an integer (user ID)
            return CustomUser.objects.filter(id=collaborator_data).first()  # Retrieve user with given ID
        elif isinstance(collaborator_data, str):  # Check if collaborator_data is a string
            if '@' in collaborator_data:  # If input is email
                return CustomUser.objects.filter(email=collaborator_data).first()  # Retrieve user with  given email
            else:  # If input is username
                return CustomUser.objects.filter(
                    username=collaborator_data).first()  # Retrieve user with given username
        else:  # If collaborator_data is not an integer or a string, return None
            raise serializers.ValidationError("Invalid collaborator data.")
    except Exception as e:
        logger.exception(e)
        raise serializers.ValidationError(str(e))


class LabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['name']
        extra_kwargs = {'user': {'required': True}}


class CustomUserUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']


class NotesSerializer(serializers.ModelSerializer):
    label = LabelsSerializer(many=True, read_only=True)  # for display collaborator by its name
    collaborator = CustomUserUsernameSerializer(many=True, read_only=True)  # for display collaborator by its email

    class Meta:
        model = Notes
        fields = ['id', 'user', 'title', 'description', 'isArchive', 'isTrash', 'color', 'image', 'label',
                  'collaborator', 'reminder']
        read_only_fields = ['label', 'collaborator']

    def create(self, validated_data):
        collaborator_data = self.initial_data.get('collaborator', [])
        collaborators = [get_collaborator(self, data) for data in collaborator_data]
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
