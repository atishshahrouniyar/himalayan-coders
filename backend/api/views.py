from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import StudentProfile, ProfessorProfile, ResearchProject, Match
from .serializers import (
    StudentProfileSerializer, ProfessorProfileSerializer, ResearchProjectSerializer, MatchSerializer,
    StudentProfileListSerializer, ProfessorProfileListSerializer, ResearchProjectListSerializer
)
from .gemini_service import GeminiMatchingService

@extend_schema_view(
    list=extend_schema(
        summary="List all students",
        description="Retrieve a paginated list of all student profiles",
        tags=['students']
    ),
    create=extend_schema(
        summary="Create a new student",
        description="Create a new student profile",
        tags=['students']
    ),
    retrieve=extend_schema(
        summary="Get student details",
        description="Retrieve detailed information about a specific student",
        tags=['students']
    ),
    update=extend_schema(
        summary="Update student",
        description="Update an existing student profile",
        tags=['students']
    ),
    destroy=extend_schema(
        summary="Delete student",
        description="Delete a student profile",
        tags=['students']
    ),
)
class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [AllowAny]  # For now, allow any access
    
    def get_serializer_class(self):
        if self.action == 'list':
            return StudentProfileListSerializer
        return StudentProfileSerializer
    
    @extend_schema(
        summary="Search students",
        description="Search students by various criteria including name, university, department, degree level, and interests",
        parameters=[
            OpenApiParameter(
                name='q',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='General search query for name, university, or department'
            ),
            OpenApiParameter(
                name='department',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by department'
            ),
            OpenApiParameter(
                name='degree_level',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by degree level (BS, MS, PhD, Other)'
            ),
            OpenApiParameter(
                name='interests',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by research interests (can be multiple)',
                many=True
            ),
        ],
        examples=[
            OpenApiExample(
                'Search by name',
                value={'q': 'John'},
                description='Search for students with "John" in their name'
            ),
            OpenApiExample(
                'Search by department',
                value={'department': 'Computer Science'},
                description='Find all students in Computer Science department'
            ),
        ],
        tags=['students']
    )
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

@extend_schema_view(
    list=extend_schema(
        summary="List all professors",
        description="Retrieve a paginated list of all professor profiles",
        tags=['professors']
    ),
    create=extend_schema(
        summary="Create a new professor",
        description="Create a new professor profile",
        tags=['professors']
    ),
    retrieve=extend_schema(
        summary="Get professor details",
        description="Retrieve detailed information about a specific professor",
        tags=['professors']
    ),
    update=extend_schema(
        summary="Update professor",
        description="Update an existing professor profile",
        tags=['professors']
    ),
    destroy=extend_schema(
        summary="Delete professor",
        description="Delete a professor profile",
        tags=['professors']
    ),
)
class ProfessorProfileViewSet(viewsets.ModelViewSet):
    queryset = ProfessorProfile.objects.all()
    serializer_class = ProfessorProfileSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProfessorProfileListSerializer
        return ProfessorProfileSerializer
    
    @extend_schema(
        summary="Search professors",
        description="Search professors by various criteria including name, title, institution, department, research areas, and student acceptance status",
        parameters=[
            OpenApiParameter(
                name='q',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='General search query for name, title, institution, or department'
            ),
            OpenApiParameter(
                name='department',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by department'
            ),
            OpenApiParameter(
                name='institution',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by institution'
            ),
            OpenApiParameter(
                name='research_areas',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by research areas (can be multiple)',
                many=True
            ),
            OpenApiParameter(
                name='accepting_students',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filter by whether professor is accepting students'
            ),
        ],
        examples=[
            OpenApiExample(
                'Search by name',
                value={'q': 'Dr. Smith'},
                description='Search for professors with "Dr. Smith" in their name'
            ),
            OpenApiExample(
                'Search by research area',
                value={'research_areas': 'Machine Learning'},
                description='Find professors working in Machine Learning'
            ),
        ],
        tags=['professors']
    )
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

@extend_schema_view(
    list=extend_schema(
        summary="List all research projects",
        description="Retrieve a paginated list of all active research projects",
        tags=['projects']
    ),
    create=extend_schema(
        summary="Create a new research project",
        description="Create a new research project",
        tags=['projects']
    ),
    retrieve=extend_schema(
        summary="Get project details",
        description="Retrieve detailed information about a specific research project",
        tags=['projects']
    ),
    update=extend_schema(
        summary="Update project",
        description="Update an existing research project",
        tags=['projects']
    ),
    destroy=extend_schema(
        summary="Delete project",
        description="Delete a research project",
        tags=['projects']
    ),
)
class ResearchProjectViewSet(viewsets.ModelViewSet):
    queryset = ResearchProject.objects.filter(isActive=True)
    serializer_class = ResearchProjectSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ResearchProjectListSerializer
        return ResearchProjectSerializer
    
    @extend_schema(
        summary="Search research projects",
        description="Search research projects by various criteria including title, summary, research areas, compensation, location, and hours",
        parameters=[
            OpenApiParameter(
                name='q',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='General search query for title, summary, or description'
            ),
            OpenApiParameter(
                name='research_areas',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by research areas (can be multiple)',
                many=True
            ),
            OpenApiParameter(
                name='compensation',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by compensation type (Paid, Unpaid, Stipend)'
            ),
            OpenApiParameter(
                name='location',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter by location'
            ),
            OpenApiParameter(
                name='min_hours',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Minimum hours per week'
            ),
            OpenApiParameter(
                name='max_hours',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Maximum hours per week'
            ),
        ],
        examples=[
            OpenApiExample(
                'Search by title',
                value={'q': 'Machine Learning'},
                description='Search for projects with "Machine Learning" in the title'
            ),
            OpenApiExample(
                'Search by compensation',
                value={'compensation': 'Paid'},
                description='Find all paid research projects'
            ),
        ],
        tags=['projects']
    )
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

@extend_schema_view(
    list=extend_schema(
        summary="List all matches",
        description="Retrieve a paginated list of all matches",
        tags=['matches']
    ),
    create=extend_schema(
        summary="Create a new match",
        description="Create a new match record",
        tags=['matches']
    ),
    retrieve=extend_schema(
        summary="Get match details",
        description="Retrieve detailed information about a specific match",
        tags=['matches']
    ),
    update=extend_schema(
        summary="Update match",
        description="Update an existing match",
        tags=['matches']
    ),
    destroy=extend_schema(
        summary="Delete match",
        description="Delete a match record",
        tags=['matches']
    ),
)
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gemini_service = GeminiMatchingService()
    
    @extend_schema(
        summary="Generate AI-enhanced matches",
        description="Generate AI-enhanced matches for a student with professors or research projects. Uses Google's Gemini AI to analyze compatibility and provide detailed scoring.",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'student_id': {
                        'type': 'string',
                        'description': 'ID of the student to generate matches for'
                    },
                    'match_type': {
                        'type': 'string',
                        'enum': ['professor', 'project'],
                        'description': 'Type of matches to generate',
                        'default': 'professor'
                    },
                    'use_ai': {
                        'type': 'boolean',
                        'description': 'Whether to use AI-enhanced matching',
                        'default': True
                    }
                },
                'required': ['student_id']
            }
        },
        examples=[
            OpenApiExample(
                'Match with professors',
                value={
                    'student_id': '1',
                    'match_type': 'professor',
                    'use_ai': True
                },
                description='Generate AI-enhanced matches with professors'
            ),
            OpenApiExample(
                'Match with projects',
                value={
                    'student_id': '1',
                    'match_type': 'project',
                    'use_ai': False
                },
                description='Generate basic matches with research projects'
            ),
        ],
        tags=['matches']
    )
    @action(detail=False, methods=['post'])
    def generate_matches(self, request):
        """Generate AI-enhanced matches for a student"""
        student_id = request.data.get('student_id')
        match_type = request.data.get('match_type', 'professor')  # 'professor' or 'project'
        use_ai = request.data.get('use_ai', True)  # Enable/disable AI enhancement
        
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
        
        # Generate AI-enhanced matches
        if match_type == 'professor':
            matches = self._match_student_to_professors(student, use_ai)
        else:
            matches = self._match_student_to_projects(student, use_ai)
        
        return Response({
            'success': True,
            'data': matches,
            'total': len(matches),
            'ai_enhanced': use_ai
        })
    
    def _match_student_to_professors(self, student, use_ai=True):
        """AI-enhanced matching algorithm for student to professors"""
        professors = ProfessorProfile.objects.filter(acceptingStudents=True)
        matches = []
        
        for professor in professors:
            if use_ai:
                # Use AI-enhanced matching
                ai_score, ai_highlights, ai_analysis = self.gemini_service.calculate_ai_match_score(
                    student_data=StudentProfileSerializer(student).data,
                    professor_data=ProfessorProfileSerializer(professor).data
                )
                
                # Generate AI explanation
                ai_explanation = self.gemini_service.generate_match_explanation(
                    student_data=StudentProfileSerializer(student).data,
                    professor_data=ProfessorProfileSerializer(professor).data,
                    match_score=ai_score
                )
                
                # Use AI score if available, otherwise fallback to basic score
                score = ai_score if ai_score > 0 else self._calculate_basic_score(student, professor)
                highlights = ai_highlights if ai_highlights else self._get_common_interests(student, professor)
                
                match = Match.objects.create(
                    student=student,
                    professor=professor,
                    matchType='professor',
                    score=score,
                    highlights=highlights,
                    studentInterests=student.primaryInterests,
                    professorInterests=professor.researchAreas,
                    availabilityFit=True,
                    levelFit=True,
                    aiScore=ai_score if ai_score > 0 else None,
                    aiExplanation=ai_explanation,
                    aiAnalysis=ai_analysis,
                    detailedScores=ai_analysis.get('detailed_scores', {})
                )
            else:
                # Use basic matching
                score = self._calculate_basic_score(student, professor)
                highlights = self._get_common_interests(student, professor)
                
                match = Match.objects.create(
                    student=student,
                    professor=professor,
                    matchType='professor',
                    score=score,
                    highlights=highlights,
                    studentInterests=student.primaryInterests,
                    professorInterests=professor.researchAreas,
                    availabilityFit=True,
                    levelFit=True
                )
            
            matches.append(MatchSerializer(match).data)
        
        # Sort by score (highest first)
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches
    
    def _match_student_to_projects(self, student, use_ai=True):
        """AI-enhanced matching algorithm for student to projects"""
        projects = ResearchProject.objects.filter(isActive=True)
        matches = []
        
        for project in projects:
            if use_ai:
                # Use AI-enhanced matching
                ai_score, ai_highlights, ai_analysis = self.gemini_service.calculate_ai_match_score(
                    student_data=StudentProfileSerializer(student).data,
                    project_data=ResearchProjectSerializer(project).data
                )
                
                # Generate AI explanation
                ai_explanation = self.gemini_service.generate_match_explanation(
                    student_data=StudentProfileSerializer(student).data,
                    project_data=ResearchProjectSerializer(project).data,
                    match_score=ai_score
                )
                
                # Use AI score if available, otherwise fallback to basic score
                score = ai_score if ai_score > 0 else self._calculate_basic_project_score(student, project)
                highlights = ai_highlights if ai_highlights else self._get_common_project_interests(student, project)
                
                match = Match.objects.create(
                    student=student,
                    project=project,
                    matchType='project',
                    score=score,
                    highlights=highlights,
                    studentInterests=student.primaryInterests,
                    professorInterests=project.professor.researchAreas,
                    availabilityFit=True,
                    levelFit=True,
                    aiScore=ai_score if ai_score > 0 else None,
                    aiExplanation=ai_explanation,
                    aiAnalysis=ai_analysis,
                    detailedScores=ai_analysis.get('detailed_scores', {})
                )
            else:
                # Use basic matching
                score = self._calculate_basic_project_score(student, project)
                highlights = self._get_common_project_interests(student, project)
                
                match = Match.objects.create(
                    student=student,
                    project=project,
                    matchType='project',
                    score=score,
                    highlights=highlights,
                    studentInterests=student.primaryInterests,
                    professorInterests=project.professor.researchAreas,
                    availabilityFit=True,
                    levelFit=True
                )
            
            matches.append(MatchSerializer(match).data)
        
        # Sort by score (highest first)
        matches.sort(key=lambda x: x['score'], reverse=True)
        return matches
    
    def _calculate_basic_score(self, student, professor):
        """Calculate basic match score based on research area overlap"""
        common_interests = set(student.primaryInterests) & set(professor.researchAreas)
        return len(common_interests) / max(len(student.primaryInterests), 1) * 100
    
    def _get_common_interests(self, student, professor):
        """Get common interests between student and professor"""
        common_interests = set(student.primaryInterests) & set(professor.researchAreas)
        return list(common_interests)
    
    def _calculate_basic_project_score(self, student, project):
        """Calculate basic match score based on project research area overlap"""
        common_interests = set(student.primaryInterests) & set(project.researchAreas)
        return len(common_interests) / max(len(student.primaryInterests), 1) * 100
    
    def _get_common_project_interests(self, student, project):
        """Get common interests between student and project"""
        common_interests = set(student.primaryInterests) & set(project.researchAreas)
        return list(common_interests)

@extend_schema_view()
class SearchViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Global search",
        description="Search across all entities (students, professors, projects) with a single query",
        parameters=[
            OpenApiParameter(
                name='q',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Search query to find across all entities',
                required=True
            ),
            OpenApiParameter(
                name='type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Type of entities to search in (students, professors, projects, all)',
                enum=['students', 'professors', 'projects', 'all'],
                default='all'
            ),
        ],
        examples=[
            OpenApiExample(
                'Search all entities',
                value={'q': 'Machine Learning'},
                description='Search for "Machine Learning" across all entities'
            ),
            OpenApiExample(
                'Search only students',
                value={'q': 'John', 'type': 'students'},
                description='Search for students with "John" in their name'
            ),
        ],
        tags=['search']
    )
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
