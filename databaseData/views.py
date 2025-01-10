# core/views.py
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.crypto import get_random_string
from django.conf import settings
from .models import EmailVerification   
from django.views import View
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
# Serializer
# ------------------------------------------------------------------------------------
class ClassDetailView(APIView):
    def get(self, request, class_id):
        try:
            # Fetch the class instance by `class_id`
            class_instance = Class.objects.get(class_id=class_id)
            
            # Access related `free_slots` using the `related_name`
            free_slots = class_instance.free_slots.all()
            
            # Prepare the response
            return Response({
                'id': class_instance.class_id,  # Use `class_id` for the primary key
                'class_name': class_instance.class_name,
                'free_slots': [
                    {'id': slot.id, 'free_slots': slot.free_slots ,'day_of_week':slot.day_of_week ,} for slot in free_slots
                ]
            })
        except Class.DoesNotExist:
            return Response({'error': 'Class not found'}, status=404)

# freeClasses
class FreeClassView(APIView):
    def get(self, request, pk=None):
        if pk:  # If a specific department ID is provided
            freeClass = get_object_or_404(FreeClassSlot, pk=pk)
            serializer = FreeClassSerializer(freeClass)
            return Response(serializer.data)
        else:  # If no ID is provided, list all departments
            freeClass = FreeClassSlot.objects.all()
            serializer = FreeClassSerializer(freeClass, many=True)
            return Response(serializer.data)
    def post(self, request):
        serializer = FreeClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, class_id, free_slots, day_of_week):
        # Ensure the class_id, slot, and day_of_week are provided
        if not class_id or not free_slots or not day_of_week:
            return Response(
                {"error": "Missing required fields: class_id, free_slots, day_of_week"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filter and delete the records that match the given criteria
        deleted_count, _ = FreeClassSlot.objects.filter(
            class_id=class_id,
            free_slots=free_slots,
            day_of_week=day_of_week
        ).delete()

        # If no records were deleted, return a 404 error
        if deleted_count == 0:
            return Response(
                {"error": "No matching records found to delete"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Return a 204 No Content status if records were successfully deleted
        return Response(status=status.HTTP_204_NO_CONTENT)
          # =========================================================================
#subjects involved
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
        teachers = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(teachers, data=request.data)
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
        subject = get_object_or_404(Subject, pk=pk)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# -------------------------------------------------------------------------------------------------

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
    def get(self, request, department_id=None):
      
        if department_id:
            users = User.objects.filter(department_id=department_id) 
            serializer = UserSerializer(users, many=True)
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

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class SendEmailView(View):
    def post(self, request, *args, **kwargs):
        try:
            message = request.POST.get('message')
            email = request.POST.get('email')
            name = request.POST.get('name')

            if not (message and email and name):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            send_mail(
                subject=f"Contact From {name}",
                message=message,
                
                from_email=settings.EMAIL_HOST_USER,  # Ensure EMAIL_HOST_USER is configured in settings.py
                recipient_list=[email],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Email sent successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
# =============================================================================
class SchedulerView(APIView):
    def get(self, request, department_id=None):
        print(department_id)
        # If department is provided, filter by it
        scheduler = Scheduler.objects.filter(department_id=department_id)

    # Check if any records were found for the given department_id
        if not scheduler.exists():
            return Response({"error": "No scheduler found for the given department."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data if records are found
        serializer = SchedulerSerializer(scheduler, many=True)
        return Response(serializer.data)

        # If no department provided, return all records
        scheduler = Scheduler.objects.all()
        serializer = SchedulerSerializer(scheduler, many=True)
        return Response(serializer.data)
    def put(self, request, pk):
        scheduler = get_object_or_404(Scheduler, pk=pk)
        serializer = SchedulerSerializer(scheduler, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('Scheduler updated successfully.')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
       
        serializer = SchedulerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, department_id):
        # Filter and delete all records that match the given department_id
        deleted_count, _ = Scheduler.objects.filter(department_id=department_id).delete()

        # If no records were deleted, return a 404 error
        if deleted_count == 0:
            return Response(
                {"error": "No matching records found to delete"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Return a 204 No Content status if records were successfully deleted
        return Response(status=status.HTTP_204_NO_CONTENT)