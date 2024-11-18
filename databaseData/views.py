# core/views.py
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Department, Class, User, Teacher , Subject
from .serializers import DepartmentSerializer, ClassSerializer, UserSerializer, TeacherSerializer , SubjectSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import EmailVerification 

class SubjectView(APIView):
     def get(self, request, pk=None):
        if pk:  # If a specific department ID is provided
            subject = get_object_or_404(Subject, pk=pk)
            serializer = SubjectSerializer(subject)
            return Response(serializer.data)
        else:  # If no ID is provided, list all departments
            subject = Subject.objects.all()
            serializer = SubjectSerializer(subject, many=True)
            return Response(serializer.data)
     def put(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Subject updated successfully.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     def delete(self, request, pk):
        subjects = get_object_or_404(Subject, pk=pk)
        subjects.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    #-------------------------------------------------------------------------------------
class TeacherView(APIView):
     def get(self, request, pk=None):
        if pk:  # If a specific department ID is provided
            teacher = get_object_or_404(Teacher, pk=pk)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        else:  # If no ID is provided, list all departments
            teacher = Teacher.objects.all()
            serializer = TeacherSerializer(teacher, many=True)
            return Response(serializer.data)
     def put(self, request, pk):
        teachers = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherSerializer(teachers, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Teacher updated successfully.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     def delete(self, request, pk):
        teachers = get_object_or_404(Teacher, pk=pk)
        teachers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# -------------------------------------------------------------------------------------------------
class UserView(APIView):
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('User updated successfully.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, pk=None):
        if pk:  # If a specific department ID is provided
            users = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(users)
            return Response(serializer.data)
        else:  # If no ID is provided, list all departments
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        classs = get_object_or_404(User, pk=pk)
        classs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#-------------------------------------------------------------------------------------------
#class classes
class ClasssView(APIView):
    
    def post(self, request):
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        classs = get_object_or_404(Class, pk=pk)
        classs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get(self, request, pk=None):
        if pk:  # If a specific department ID is provided
            classs = get_object_or_404(Department, pk=pk)
            serializer = ClassSerializer(classs)
            return Response(serializer.data)
        else:  # If no ID is provided, list all departments
            classs = Class.objects.all()
            serializer = ClassSerializer(classs, many=True)
            return Response(serializer.data)
        
    def getClassRoutes(request):
        routes =[{
                'Endpoint': '/classs/createClass/',
                'method': 'POST',
                'class_name' : {'class_name' : "" },
                'class_type':{'class_type':""},
                'department':{'department'},
                'description': 'create new department'
            },{
                'Endpoint': '/classs/id/updateClass/',
                'method': 'PUT',
                'class_name' : {'class_name' : "" },
                'class_type':{'class_type':""},
                'department':{'department'},
                'description': 'update an existing department'
            },
            ]
        return Response(routes)
    def put(self, request, pk):
        classs = get_object_or_404(Class, pk=pk)
        serializer = ClassSerializer(classs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Department updated successfully.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 #nazikka maya   
# department views
class DepartmentView(APIView):
    @api_view(['GET'])
    def getDepartmentroutes(request):
        routes = [
            # routes for department
            {
                'Endpoint': '/department/',
                'method': 'GET',
                'department_name' : None,
                'description': 'Returns an array of department'
            },
            {
                'Endpoint': '/department/id/',
                'method': 'GET',
                'department_name' : None,
                'description': 'Returns a specific department'
            },
            {
                'Endpoint': '/department/createDepartment/',
                'method': 'POST',
                'department_name' : {'department_name' : ""},
                'description': 'create new department'
            },
            {
                'Endpoint': '/department/id/updateDepartment/',
                'method': 'PUT',
                'department_name' : {'department_name' : ""},
                'description': 'update an existing department'
            },
            {
                'Endpoint': '/department/deleteDepartment',
                'method': 'DELETE',
                'department_name' : None,
                'description': 'delete an existing department'
            },
            # define other routes here:

            # {

            # },

            # {

            # }
        ]
        return Response(routes)
    # Handles GET for listing and retrieving departments
    def get(self, request, pk=None):
        if pk:  # If a specific department ID is provided
            department = get_object_or_404(Department, pk=pk)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data)
        else:  # If no ID is provided, list all departments
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            return Response(serializer.data)

    # Handles POST for creating a new department
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handles PUT for updating an existing department
    def put(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Department updated successfully.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handles DELETE for removing an existing department
    def delete(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#---------------------------------------------------------------------------------------
# views.py in Django


# Model for storing pending email verifications


def initiate_email_verification(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'status': 'error', 'message': 'Email is required'}, status=400)

    # Generate a unique verification token
    token = get_random_string(20)
    verification, created = EmailVerification.objects.get_or_create(email=email, defaults={'token': token})
    if not created:
        verification.token = token
        verification.save()
    
    # Send a verification email
    verification_url = f'{settings.FRONTEND_URL}/verify-email/?token={token}'
    send_mail(
        'Verify your email',
        f'Please confirm that this is your email by clicking on the following link: {verification_url}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
    )
    return JsonResponse({'status': 'success', 'message': 'Verification email sent'})

def verify_email(request):
    token = request.GET.get('token')
    if not token:
        return JsonResponse({'status': 'error', 'message': 'Token is required'}, status=400)

    try:
        verification = EmailVerification.objects.get(token=token)
        verification.is_verified = True
        verification.save()
        return JsonResponse({'status': 'success', 'message': 'Email verified successfully'})
    except EmailVerification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid token'}, status=400)
