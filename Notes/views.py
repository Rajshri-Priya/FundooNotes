from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from Notes.models import Notes, Labels
from Notes.redis_utils import RedisCrud
from Notes.serializers import NotesSerializer, LabelsSerializer
from logging_confiq.logger import get_logger
from user_auth.models import CustomUser
from Notes.serializers import get_collaborator

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

            # Store note data in Redis
            RedisCrud().save_note_in_redis(serializer.data, request.user.id)
            return Response(
                {"success": True, "message": "Note Created Successfully", "data": serializer.data, "status": 200},
                status=200)
        except Exception as e:
            # logger.exception(e.args[0])==> print specific exception message
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def get(self, request):
        try:
            # retrieve note data in by user
            redis_data = RedisCrud().get_notes_by_user_id(request.user)
            if redis_data:
                return Response(
                    {"success": True, "message": "Note Retrieved Successfully", "data": redis_data, "status": 200},
                    status=200)

            # notes = Notes.objects.filter(user=request.user)
            notes = Notes.objects.filter(Q(user__id=request.user.id) | Q(collaborator__id=request.user.id)).distinct()
            serializer = NotesSerializer(notes, many=True)
            return Response(
                {"success": True, "message": "Note Retrieved Successfully", "data": serializer.data, "status": 200},
                status=200)
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

            # Store updated note data in Redis
            RedisCrud().update_note_in_redis(note_id, request.data, request.user.id)

            return Response({"success": True, 'message': 'Note updated successfully!', 'Data': serializer.data,
                             "status": 200}, status=200)

        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    # @swagger_auto_schema(request_body=NotesSerializer, operation_summary='DELETE Add Notes')
    def delete(self, request, note_id):
        try:
            notes = Notes.objects.get(id=note_id)
            notes.delete()

            RedisCrud().delete_note_in_redis(note_id, request.user)

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
                             "status": 200}, status=200)
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
                             'status': 200}, status=200)

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
            notes = Notes.objects.get(id=note_id, user=request.user).first()
            if notes:
                if notes.isArchive == False:
                    notes.isArchive = True
                else:
                    notes.isArchive = False
                    return Response({"success": False, 'message': 'isArchived updated not successfully!'}, status=200)
                notes.save()
                return Response({"success": True, 'message': 'isArchived updated successfully!'}, status=200)
            else:
                return Response({"success": False, 'message': 'Note does not exist or does not belong to user!'},
                                status=400)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def get(self, request):
        try:
            notes = Notes.objects.filter(user=request.user, isArchive=True)
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
            notes = Notes.objects.get(id=note_id, user=request.user)
            if notes:
                if notes.isTrash == False:
                    notes.isTrash = True
                else:
                    notes.isTrash = False
                    return Response({'success': False, 'message': 'Notes isTrash unsuccessful!'}, status=200)
                notes.save()
                return Response({'success': True, 'message': 'Notes isTrash successful!'}, status=200)
            else:
                return Response({"success": False, 'message': 'Note does not exist or does not belong to user!'},
                                status=400)

        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def get(self, request):
        try:

            notes = Notes.objects.filter(user=request.user, isTrash=True)
            serializer = NotesSerializer(notes, many=True)
            return Response({"success": True, 'message': 'isTrash retrieve successfully!', 'Data': serializer.data,
                             'status': 201}, status=201)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


class NotesCollaboratorAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            note_id = request.data.get('note_id')
            note = Notes.objects.get(pk=note_id)

            collaborator_data = request.data.get('collaborator')
            if collaborator_data is not None:
                collaborator = get_collaborator(self, collaborator_data)
            else:
                return Response({'message': 'Collaborator data is missing.'}, status=400)

            note.collaborator.add(collaborator)

            return Response({'message': f'Added collaborator with id {collaborator} to note with id {note_id}'},
                            status=200)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def delete(self, request):
        try:
            note_id = request.data.get('note_id')
            note = Notes.objects.get(pk=note_id)
            collaborator_data = request.data.get('collaborator')
            if collaborator_data is None:
                return Response({'message': 'Collaborator data is missing.'}, status=400)

            collaborator = get_collaborator(self, collaborator_data)
            if collaborator in note.collaborator.all():
                note.collaborator.remove(collaborator)
                return Response(
                    {'message':f'Successfully removed collaborator with {collaborator} from note with id {note_id}'},
                    status=200)
            else:
                return Response(
                    {'message': f'Collaborator with id {collaborator} is not associated with note with id {note_id}'},
                    status=400)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400})
