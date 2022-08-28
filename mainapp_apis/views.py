from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from mainapp_apis.serializer import StudentSerializer, TeacherSerializer
from mainapp_apis.models import StudentsModels
from rest_framework import viewsets, status
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend



class TeacherViewSet(viewsets.ViewSet):
    """
    methods for teacher 
    """
    serializer_class = TeacherSerializer
    permission_classes = (AllowAny, )

    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)

#view to filter students with student_id
class StudentsList(ListAPIView):
        queryset= StudentsModels.objects.all()
        serializer_class = StudentSerializer
        
        filter_backend = [DjangoFilterBackend]
        filter_fields = ['student_id']

class StudentViewSet(viewsets.ViewSet):
    """
    methods for students 
    """
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer


    def create(self, request):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Student successfully registered!',
                'student': serializer.data
            }

        return Response(response, status=status_code)


    def retrieve(self, request, pk=None):
        studentDetails=get_object_or_404(StudentsModels,pk=pk)
        serializer = self.serializer_class(studentDetails)
        
        return Response(serializer.data)

    def update(self, request, pk=None):
        studentsDetails = StudentsModels.objects.get(student_id=pk)

        serializer = self.serializer_class(studentsDetails,data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Student details updated!',
                'user': serializer.data
            }

        return Response(response, status=status_code)

    def destroy(self, request, pk=None):
        studentDetails=get_object_or_404(StudentsModels,pk=pk)
        studentDetails.delete()

        status_code = status.HTTP_204_NO_CONTENT
        response = {
                'success': True,
                'statusCode': status_code,
                'message': 'Student deleted!',
            }

        return Response(response, status=status_code)