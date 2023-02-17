from rest_framework import serializers
from Notes.models import Notes, Labels


class LabelsSerializer(serializers.ModelSerializer):
    """
        Labels Serializer : name
    """

    # name = serializers.CharField(min_length=2, max_length=200, required=True)

    class Meta:
        model = Labels
        fields = ['name', 'user']


class DisplayLabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labels
        fields = ['name']


class NotesSerializer(serializers.ModelSerializer):
    label = DisplayLabelsSerializer(many=True, read_only=True)

    class Meta:
        model = Notes
        fields = ['id', 'user', 'title', 'description', 'isArchive', 'isTrash', 'color', 'image', 'label',
                  'collaborator', 'reminder']
        read_only_fields = ['label','collaborator']

    def create(self, validated_data):
        print(validated_data)
        label_name = self.initial_data.get('label')
        notes = Notes.objects.create(**validated_data)
        label = Labels.objects.filter(name=label_name)
        if label.exists():
            notes.label.add(label.first())
            return notes

        label = Labels.objects.create(name=label_name, user=validated_data.get("user"))
        notes.label.add(label)
        return notes

