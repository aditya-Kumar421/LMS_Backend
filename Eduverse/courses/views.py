from rest_framework.response import Response
from courses.models import Sector, Course
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CourseDisplaySerializer, CourseUnpaidSerializer, CourseListSerailizer
from django.http import HttpResponseBadRequest
from django.db.models import Q

# Create your views here.
#Dashboard for courses
class CoursesHomeView(APIView):
    def get(self, request, *args, **kwargs):
        sectors=Sector.objects.order_by("?")[:6]

        sector_response=[]

        for sector in sectors:
            sector_courses=sector.related_course.order_by("?")[:4]
            courses_serializer=CourseDisplaySerializer(sector_courses, many=True)

            sector_obj={
                'sector_name':sector.name,
                'sector_uuid':sector.sector_uuid,
                'featured_course':courses_serializer.data,
                'sector_image':sector.get_image_absolute_url()
            }

            sector_response.append(sector_obj)
        
        return Response(data=sector_response, status=status.HTTP_200_OK)

#Details of courses
class CourseDetail(APIView):
    def get(self, request, course_uuid, *args, **kwargs):
        course =Course.objects.filter(course_uuid=course_uuid)

        if not course:
            return HttpResponseBadRequest('course does not exist')

        serializer=CourseUnpaidSerializer(course[0])

        return Response(data=serializer.data, status=status.HTTP_200_OK)

#categories for courses
class SectorCourse(APIView):
    def get(self, request, sector_uuid, *args, **kwargs):
        sector=Sector.objects.filter(sector_uuid=sector_uuid)

        if not sector:
            return HttpResponseBadRequest('Sector does not exist')
        
        sector_courses=sector[0].related_course.all()
        serializer=CourseListSerailizer(sector_courses, many=True)

        total_students=0
        for course in sector_courses:
            total_students+=course.get_enrolled_student()

        return Response({
            'data':serializer.data,
            'sector_name': sector[0].name,
            'total_students':total_students,
            },status=status.HTTP_200_OK )
    
#Search bar for courses:
class SearchCourse(APIView):
    def get(self, request, search_term):
        matches=Course.objects.filter(Q(title__icontains=search_term)| Q(description__icontains=search_term))
        serializer=CourseListSerailizer(matches, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)