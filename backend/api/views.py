from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import StudentProfile, ProfessorProfile, ResearchProject, Match
from .serializers import (
    StudentProfileSerializer, ProfessorProfileSerializer, ResearchProjectSerializer, MatchSerializer,
    StudentProfileListSerializer, ProfessorProfileListSerializer, ResearchProjectListSerializer
)

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]  # For now, allow any access
    
    def get_serializer_class(self):
        if self.action == 'list':
            return StudentProfileListSerializer
        return StudentProfileSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search students by various criteria"""
        query = request.query_params.get('q', '')
        department = request.query_params.get('department', '')
        degree_level = request.query_params.get('degree_level', '')
        interests = request.query_params.getlist('interests', [])
        
        queryset = self.queryset
        
        if query:
            queryset = queryset.filter(
                Q(firstName__icontains=query) |
                Q(lastName__icontains=query) |
                Q(university__icontains=query) |
                Q(department__icontains=query)
            )
        
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        if degree_level:
            queryset = queryset.filter(degreeLevel=degree_level)
        
        if interests:
            queryset = queryset.filter(primaryInterests__overlap=interests)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'total': queryset.count()
        })

class ProfessorProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfessorProfile.objects.all()
    serializer_class = ProfessorProfileSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProfessorProfileListSerializer
        return ProfessorProfileSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search professors by various criteria"""
        query = request.query_params.get('q', '')
        department = request.query_params.get('department', '')
        institution = request.query_params.get('institution', '')
        research_areas = request.query_params.getlist('research_areas', [])
        accepting_students = request.query_params.get('accepting_students', '')
        
        queryset = self.queryset
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(title__icontains=query) |
                Q(institution__icontains=query) |
                Q(department__icontains=query)
            )
        
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        if institution:
            queryset = queryset.filter(institution__icontains=institution)
        
        if research_areas:
            queryset = queryset.filter(researchAreas__overlap=research_areas)
        
        if accepting_students:
            queryset = queryset.filter(acceptingStudents=accepting_students.lower() == 'true')
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'total': queryset.count()
        })

class ResearchProjectViewSet(viewsets.ModelViewSet):
    queryset = ResearchProject.objects.filter(isActive=True)
    serializer_class = ResearchProjectSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ResearchProjectListSerializer
        return ResearchProjectSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search research projects by various criteria"""
        query = request.query_params.get('q', '')
        research_areas = request.query_params.getlist('research_areas', [])
        compensation = request.query_params.get('compensation', '')
        location = request.query_params.get('location', '')
        min_hours = request.query_params.get('min_hours', '')
        max_hours = request.query_params.get('max_hours', '')
        
        queryset = self.queryset
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(description__icontains=query)
            )
        
        if research_areas:
            queryset = queryset.filter(researchAreas__overlap=research_areas)
        
        if compensation:
            queryset = queryset.filter(compensation=compensation)
        
        if location:
            queryset = queryset.filter(location=location)
        
        if min_hours:
            queryset = queryset.filter(hoursPerWeek__gte=int(min_hours))
        
        if max_hours:
            queryset = queryset.filter(hoursPerWeek__lte=int(max_hours))
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'total': queryset.count()
        })

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def generate_matches(self, request):
        """Generate matches for a student"""
        student_id = request.data.get('student_id')
        match_type = request.data.get('match_type', 'professor')  # 'professor' or 'project'
        
        if not student_id:
            return Response({
                'success': False,
                'message': 'student_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            student = StudentProfile.objects.get(id=student_id)
        except StudentProfile.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Student not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Simple matching algorithm (can be enhanced)
        if match_type == 'professor':
            matches = self._match_student_to_professors(student)
        else:
            matches = self._match_student_to_projects(student)
        
        return Response({
            'success': True,
            'data': matches,
            'total': len(matches)
        })
    
    def _match_student_to_professors(self, student):
        """Simple matching algorithm for student to professors"""
        professors = ProfessorProfile.objects.filter(acceptingStudents=True)
        matches = []
        
        for professor in professors:
            # Calculate basic match score based on research area overlap
            common_interests = set(student.primaryInterests) & set(professor.researchAreas)
            score = len(common_interests) / max(len(student.primaryInterests), 1) * 100
            
            if score > 0:  # Only include matches with some overlap
                match = Match.objects.create(
                    student=student,
                    professor=professor,
                    matchType='professor',
                    score=score,
                    highlights=list(common_interests),
                    studentInterests=student.primaryInterests,
                    professorInterests=professor.researchAreas,
                    availabilityFit=True,  # Simplified for now
                    levelFit=True  # Simplified for now
                )
                matches.append(MatchSerializer(match).data)
        
        return matches
    
    def _match_student_to_projects(self, student):
        """Simple matching algorithm for student to projects"""
        projects = ResearchProject.objects.filter(isActive=True)
        matches = []
        
        for project in projects:
            # Calculate basic match score based on research area overlap
            common_interests = set(student.primaryInterests) & set(project.researchAreas)
            score = len(common_interests) / max(len(student.primaryInterests), 1) * 100
            
            if score > 0:  # Only include matches with some overlap
                match = Match.objects.create(
                    student=student,
                    project=project,
                    matchType='project',
                    score=score,
                    highlights=list(common_interests),
                    studentInterests=student.primaryInterests,
                    professorInterests=project.professor.researchAreas,
                    availabilityFit=True,  # Simplified for now
                    levelFit=True  # Simplified for now
                )
                matches.append(MatchSerializer(match).data)
        
        return matches

# Additional utility views
class SearchViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def global_search(self, request):
        """Global search across all entities"""
        query = request.query_params.get('q', '')
        entity_type = request.query_params.get('type', 'all')  # 'students', 'professors', 'projects', 'all'
        
        if not query:
            return Response({
                'success': False,
                'message': 'Query parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = {
            'students': [],
            'professors': [],
            'projects': []
        }
        
        if entity_type in ['students', 'all']:
            students = StudentProfile.objects.filter(
                Q(firstName__icontains=query) |
                Q(lastName__icontains=query) |
                Q(university__icontains=query) |
                Q(department__icontains=query)
            )[:10]
            results['students'] = StudentProfileListSerializer(students, many=True).data
        
        if entity_type in ['professors', 'all']:
            professors = ProfessorProfile.objects.filter(
                Q(name__icontains=query) |
                Q(institution__icontains=query) |
                Q(department__icontains=query)
            )[:10]
            results['professors'] = ProfessorProfileListSerializer(professors, many=True).data
        
        if entity_type in ['projects', 'all']:
            projects = ResearchProject.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query)
            )[:10]
            results['projects'] = ResearchProjectListSerializer(projects, many=True).data
        
        return Response({
            'success': True,
            'data': results,
            'query': query
        })
