from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenRefreshView

from Notes.models import Notes, Labels
from Notes.serializers import NotesSerializer,  LabelsSerializer
from logging_confiq.logger import get_logger

# logger config
logger = get_logger()


# Create your views here.
class NotesAPIView(APIView):
    serializer_class = NotesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='POST Add Notes')
    def post(self, request):
        try:
            request.data.update({'user': request.user.id})
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {"success": True, "message": "Note Created Successfully", "data": serializer.data, "status": 201},
                status=201)
        except Exception as e:
            # logger.exception(e.args[0])==> print specific exception message
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def get(self, request):
        try:
            notes = Notes.objects.filter(user=request.user)
            serializer = NotesSerializer(notes, many=True)
            return Response(
                {"success": True, "message": "Note Retrieved Successfully", "data": serializer.data, "status": 201},
                status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='PUT Update Notes')
    def put(self, request, note_id):
        try:
            request.data.update({'user': request.user.id})
            notes = Notes.objects.get(id=note_id)
            serializer = NotesSerializer(notes, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": True, 'message': 'Note updated successfully!', 'Data': serializer.data,
                             "status": 201}, status=201)

        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    # @swagger_auto_schema(request_body=NotesSerializer, operation_summary='DELETE Add Notes')
    def delete(self, request, note_id):
        try:
            notes = Notes.objects.get(id=note_id)
            notes.delete()
            return Response({"success": True, "Message": "Note Deleted Successfully", "status": 200}, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


class LabelsAPIView(APIView):
    serializer_class = LabelsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LabelsSerializer, operation_summary='POST Add Labels')
    def post(self, request):
        try:
            serializer = LabelsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            #serializer.save()
            return Response({"success": True, "message": "Label Added Successfully", "data": serializer.data,
                             "status": 201}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def get(self, request):
        try:
            labels = Labels.objects.filter(user=request.user)
            serializer = LabelsSerializer(labels, many=True)
            return Response({"success": True, "message": "Label retrieve Successfully", "data": serializer.data,
                             "status": 201}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    @swagger_auto_schema(request_body=LabelsSerializer, operation_summary='PUT Update Labels')
    def put(self, request, label_name):
        try:
            label = Labels.objects.get(name=label_name, user=request.user)
            serializer = LabelsSerializer(label, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": True, 'message': 'Labels updated successfully!', 'Data': serializer.data,
                             'status': 201}, status=201)

        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    # @swagger_auto_schema(request_body=DisplayLabelsSerializer, operation_summary='DELETE Labels')
    def delete(self, request, label_name):
        try:
            labels = Labels.objects.get(name=label_name, user=request.user)
            labels.delete()
            return Response({"success": True, "Message": "Labels Deleted Successfully"}, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


class ArchiveNoteList(APIView):
    serializer_class = NotesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='PUT Add Archive')
    def put(self, request, note_id):
        try:
            notes = Notes.objects.get(id=note_id)
            if notes.isArchive == False:
                notes.isArchive = True

            else:
                notes.isArchive = False
                return Response({"success": False, 'message': 'isArchived updated not successfully!'}, status=200)
            notes.save()
            return Response({"success": True, 'message': 'isArchived updated successfully!'}, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def get(self, request):
        try:
            notes = Notes.objects.filter(isArchive=True)
            serializer = NotesSerializer(notes, many=True)
            return Response({"success": True, 'message': 'isArchived retrieve successfully!', 'Data': serializer.data,
                             'status': 201}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


class TrashNotesAPIView(APIView):
    serializer_class = NotesSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=NotesSerializer, operation_summary='PUT Trash')
    def put(self, request, note_id):
        try:
            notes = Notes.objects.get(id=note_id)
            if notes.isTrash == False:
                notes.isTrash = True
            else:
                notes.isTrash = False
                return Response({'success': False, 'message': 'Notes isTrash unsuccessful!'}, status=200)
            notes.save()
            return Response({'success': True, 'message': 'Notes isTrash successful!'}, status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def get(self, request):
        try:
            notes = Notes.objects.filter(isTrash=True)
            serializer = NotesSerializer(notes, many=True)
            return Response({"success": True, 'message': 'isTrash retrieve successfully!', 'Data': serializer.data,
                             'status': 201}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


