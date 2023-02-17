from rest_framework.response import Response
from rest_framework.views import APIView
from Notes.models import Notes, Labels
from Notes.serializers import NotesSerializer, LabelsSerializer
from logging_confiq.logger import get_logger

# logger config
logger = get_logger()


# Create your views here.
class NotesAPIView(APIView):
    serializer_class = NotesSerializer

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

    def delete(self, request, note_id):
        try:
            notes = Notes.objects.get(id=note_id)
            notes.delete()
            return Response({"success": True, "Message": "Note Deleted Successfully", "status": 204}, status=204)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


class LabelsAPIView(APIView):
    serializer_class = LabelsSerializer

    def post(self, request):
        try:
            serializer = LabelsSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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

    def put(self, request, labels):
        try:
            serializer = LabelsSerializer(labels, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": True, 'message': 'Labels updated successfully!', 'Data': serializer.data,
                             'status': 201}, status=201)

        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)

    def delete(self, request, pk):
        try:
            labels = Labels.objects.get(id=pk)
            labels.delete()
            return Response({"success": True, "Message": "Labels Deleted Successfully"}, status=204)
        except Exception as e:
            logger.exception(e)
            return Response({"success": False, "message": str(e), "status": 400}, status=400)


class ArchiveNoteList(APIView):
    serializer_class = LabelsSerializer

    # put method
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
