from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from Notes.models import Notes
from Notes.serializers import NotesSerializer
from user_auth.models import CustomUser


# Create your views here.
class NotesAPIView(APIView):

    def post(self, request):
        try:
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Registered Successfully", "data": serializer.data, "status": 201}, status=201)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def get(self, request):
        try:
            user_auth_id = request.query_params.get('user')
            notes = Notes.objects.filter(user_id=user_auth_id)
            serializer = NotesSerializer(notes, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def put(self, request):
        try:
            user_auth_id = request.data.get('user')
            pk = request.data.get('id')
            notes = Notes.objects.get(user_id=user_auth_id, id=pk)
            serializer = NotesSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Note updated successfully!', 'Data': serializer.data})

        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def delete(self, request):
        try:
            user_auth_id = request.data.get('user')
            pk = request.data.get('id')
            notes = Notes.objects.get(user_id=user_auth_id, id=pk)
            notes.delete()
            return Response({"Message": "Note Deleted Successfully"}, status=204)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
