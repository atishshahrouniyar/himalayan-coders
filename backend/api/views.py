from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import StudentProfile, ProfessorProfile, Match
from .serializers import (
    StudentProfileSerializer, ProfessorProfileSerializer, MatchSerializer,
    StudentProfileListSerializer, ProfessorProfileListSerializer
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
        summary="Create a new professor profile",
        description="Create a new professor profile with the provided data",
        tags=['professors']
    ),
    retrieve=extend_schema(
        summary="Get a specific professor profile",
        description="Retrieve detailed information about a specific professor",
        tags=['professors']
    ),
    update=extend_schema(
        summary="Update a professor profile",
        description="Update an existing professor profile with new data",
        tags=['professors']
    ),
    destroy=extend_schema(
        summary="Delete a professor profile",
        description="Permanently delete a professor profile",
        tags=['professors']
    )
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
        description="Search professors by various criteria including name, research areas, department, and accepting students status",
        parameters=[
            OpenApiParameter(name='query', type=OpenApiTypes.STR, description='Search query for name or research areas'),
            OpenApiParameter(name='tags', type=OpenApiTypes.STR, description='Comma-separated research areas'),
            OpenApiParameter(name='department', type=OpenApiTypes.STR, description='Department filter'),
            OpenApiParameter(name='accepting_students', type=OpenApiTypes.BOOL, description='Filter by accepting students status'),
        ],
        examples=[
            OpenApiExample(
                'Search by name',
                description='Search for professors with "Machine Learning" in their name or research areas',
                value={'query': 'Machine Learning'}
            ),
            OpenApiExample(
                'Filter by department',
                description='Find all professors in Computer Science department',
                value={'department': 'Computer Science'}
            ),
            OpenApiExample(
                'Filter by accepting students',
                description='Find all professors currently accepting students',
                value={'accepting_students': True}
            )
        ],
        tags=['professors']
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search professors by various criteria"""
        query = request.query_params.get('query', '')
        tags = request.query_params.get('tags', '').split(',') if request.query_params.get('tags') else []
        department = request.query_params.get('department', '')
        accepting_students = request.query_params.get('accepting_students')

        queryset = self.get_queryset()

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(researchAreas__overlap=[query])
            )

        if tags:
            queryset = queryset.filter(researchAreas__overlap=tags)

        if department:
            queryset = queryset.filter(department__icontains=department)

        if accepting_students is not None:
            accepting_students = accepting_students.lower() == 'true'
            queryset = queryset.filter(acceptingStudents=accepting_students)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@extend_schema_view(
    list=extend_schema(
        summary="List all matches",
        description="Retrieve a paginated list of all student-professor matches",
        tags=['matches']
    ),
    create=extend_schema(
        summary="Create a new match",
        description="Create a new match between a student and professor",
        tags=['matches']
    ),
    retrieve=extend_schema(
        summary="Get a specific match",
        description="Retrieve detailed information about a specific match",
        tags=['matches']
    ),
    update=extend_schema(
        summary="Update a match",
        description="Update an existing match with new data",
        tags=['matches']
    ),
    destroy=extend_schema(
        summary="Delete a match",
        description="Permanently delete a match",
        tags=['matches']
    )
)
class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Generate AI matches",
        description="Generate AI-enhanced matches for a student with professors. Uses Google's Gemini AI to analyze compatibility and provide detailed scoring.",
        parameters=[
            OpenApiParameter(name='student_id', type=OpenApiTypes.STR, required=True, description='ID of the student to match'),
            OpenApiParameter(name='use_ai', type=OpenApiTypes.BOOL, description='Whether to use AI for enhanced matching', default=True),
        ],
        examples=[
            OpenApiExample(
                'Generate matches for student',
                description='Generate AI-enhanced matches for a specific student',
                value={'student_id': 'uuid-here', 'use_ai': True}
            ),
            OpenApiExample(
                'Generate basic matches',
                description='Generate basic matches without AI enhancement',
                value={'student_id': 'uuid-here', 'use_ai': False}
            )
        ],
        tags=['matches']
    )
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """Generate AI-enhanced matches for a student"""
        student_id = request.data.get('student_id')
        use_ai = request.data.get('use_ai', True)

        if not student_id:
            return Response({'error': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = StudentProfile.objects.get(id=student_id)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        # Generate matches
        matches = self._match_student_to_professors(student, use_ai)
        
        serializer = self.get_serializer(matches, many=True)
        return Response(serializer.data)

    def _match_student_to_professors(self, student, use_ai=True):
        """AI-enhanced matching algorithm for student to professors"""
        professors = ProfessorProfile.objects.filter(acceptingStudents=True)
        matches = []

        for professor in professors:
            # Basic scoring
            score = self._calculate_basic_score(student, professor)
            
            # AI-enhanced analysis
            ai_score = None
            ai_explanation = ""
            ai_analysis = {}
            detailed_scores = {}

            if use_ai:
                try:
                    gemini_service = GeminiMatchingService()
                    ai_result = gemini_service.analyze_match(student, professor)
                    ai_score = ai_result.get('score', score)
                    ai_explanation = ai_result.get('explanation', '')
                    ai_analysis = ai_result.get('analysis', {})
                    detailed_scores = ai_result.get('detailed_scores', {})
                except Exception as e:
                    print(f"AI analysis failed: {e}")
                    ai_score = score

            # Create match
            match = Match.objects.create(
                student=student,
                professor=professor,
                score=score,
                aiScore=ai_score,
                aiExplanation=ai_explanation,
                aiAnalysis=ai_analysis,
                detailedScores=detailed_scores,
                highlights=self._generate_highlights(student, professor),
                studentInterests=student.primaryInterests,
                professorInterests=professor.researchAreas
            )
            matches.append(match)

        return matches

    def _calculate_basic_score(self, student, professor):
        """Calculate basic compatibility score"""
        score = 0
        
        # Research area overlap
        common_areas = set(student.primaryInterests) & set(professor.researchAreas)
        if common_areas:
            score += len(common_areas) * 20
        
        # Method overlap
        common_methods = set(student.methods) & set(professor.methods)
        if common_methods:
            score += len(common_methods) * 15
        
        # Degree level compatibility
        if student.degreeLevel in professor.preferredDegreeLevels:
            score += 25
        
        # Availability compatibility
        if student.hoursPerWeek >= 10:  # Assuming minimum requirement
            score += 20
        
        return min(score, 100)

    def _generate_highlights(self, student, professor):
        """Generate match highlights"""
        highlights = []
        
        common_areas = set(student.primaryInterests) & set(professor.researchAreas)
        if common_areas:
            highlights.append(f"Shared research interests: {', '.join(common_areas)}")
        
        common_methods = set(student.methods) & set(professor.methods)
        if common_methods:
            highlights.append(f"Common methodologies: {', '.join(common_methods)}")
        
        if student.degreeLevel in professor.preferredDegreeLevels:
            highlights.append(f"Degree level compatibility: {student.degreeLevel}")
        
        return highlights

@extend_schema_view(
    list=extend_schema(
        summary="Global search",
        description="Search across all entities (students, professors) with a single query",
        parameters=[
            OpenApiParameter(name='query', type=OpenApiTypes.STR, required=True, description='Search query'),
            OpenApiParameter(
                name='type', 
                type=OpenApiTypes.STR, 
                description='Type of entities to search in (students, professors, all)',
                enum=['students', 'professors', 'all'],
                default='all'
            ),
        ],
        examples=[
            OpenApiExample(
                'Search all entities',
                description='Search for "Machine Learning" across all entities',
                value={'query': 'Machine Learning', 'type': 'all'}
            ),
            OpenApiExample(
                'Search only professors',
                description='Search for "Computer Science" professors only',
                value={'query': 'Computer Science', 'type': 'professors'}
            ),
            OpenApiExample(
                'Search only students',
                description='Search for "PhD" students only',
                value={'query': 'PhD', 'type': 'students'}
            )
        ],
        tags=['search']
    )
)
class SearchViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def global_search(self, request):
        """Global search across all entities"""
        query = request.query_params.get('query', '')
        entity_type = request.query_params.get('type', 'all')  # 'students', 'professors', 'all'
        
        if not query:
            return Response({'error': 'query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        results = {
            'students': [],
            'professors': []
        }
        
        # Search students
        if entity_type in ['students', 'all']:
            students = StudentProfile.objects.filter(
                Q(firstName__icontains=query) |
                Q(lastName__icontains=query) |
                Q(primaryInterests__overlap=[query]) |
                Q(department__icontains=query) |
                Q(university__icontains=query)
            )
            results['students'] = StudentProfileListSerializer(students, many=True).data
        
        # Search professors
        if entity_type in ['professors', 'all']:
            professors = ProfessorProfile.objects.filter(
                Q(name__icontains=query) |
                Q(researchAreas__overlap=[query]) |
                Q(department__icontains=query) |
                Q(institution__icontains=query)
            )
            results['professors'] = ProfessorProfileListSerializer(professors, many=True).data
        
        return Response(results)
