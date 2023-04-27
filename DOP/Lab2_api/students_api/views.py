from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework import decorators
from rest_framework.response import Response

from .models import Student, Course
from .serializers import StudentSerializer, CourseSerializer




class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
    def get_queryset(self, request=None):
        if request:
            qp = request.query_params
            lower_bound, upper_bound, subject, group = qp.get('lower'), qp.get('upper'), qp.get('subject', None), qp.get('group')
            courses = self.queryset
            if group and not subject:
                return Student.objects.filter(group=group)
            if group:
                courses = Course.objects.select_related('student').filter(student__group=group)
            if subject:
                courses = Course.objects.select_related('student'). \
                                            filter(mark__gte = lower_bound). \
                                            filter(mark__lte = upper_bound). \
                                            filter(name__contains=subject)
            
            return Student.objects.filter(id__in=courses.values('student_id'))
        else:
            return Student.objects.all()
        
    
    
    def create(self, request, pk = None, *args, **kwargs):
        student_data = {
            "student_id": request.data['student_id'],
            "first_name": request.data['first_name'],
            "last_name": request.data['last_name'],
            "group": request.data['group']
        }
        student = Student.objects.create(**student_data)
        if pk:
            student.id = pk
        student.save()
        for item in request.data['courses']:
            item['student'] = student
            course = Course.objects.create(**item)
            course.save()
        data = StudentSerializer(student, many=False).data

        return Response(data)
    
    
    
    def list(self, request, *args, **kwargs):
        if request.query_params:
            queryset = self.get_queryset(request)
        else:
            queryset = self.get_queryset()
        return Response(StudentSerializer(queryset, many=True).data)
    
    def destroy(self, request, *args, **kwargs):
        if request.query_params:
            queryset = self.get_queryset(request)
        else:
            queryset = self.queryset
        queryset.all().delete()
        return Response("Deleting success", 200)

   