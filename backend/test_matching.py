#!/usr/bin/env python
"""
Simple test script for the matching service
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grad_matcher.settings')
django.setup()

from api.models import StudentProfile, ProfessorProfile, Match
from api.matching_service import MatchingService

def test_matching_service():
    """Test the matching service"""
    print("Testing Matching Service...")
    
    # Get or create a test student
    student, created = StudentProfile.objects.get_or_create(
        email='test@example.com',
        defaults={
            'firstName': 'Test',
            'lastName': 'Student',
            'university': 'Test University',
            'department': 'Computer Science',
            'degreeLevel': 'BS',
            'primaryInterests': ['Machine Learning', 'Data Science'],
            'methods': ['Python', 'Statistics'],
            'programmingSkills': ['Python', 'R', 'SQL'],
            'labSkills': ['Data Analysis'],
            'statisticalSkills': ['Regression', 'Classification'],
            'hoursPerWeek': 20,
            'compensation': 'Unpaid',
            'remotePreference': 'Hybrid'
        }
    )
    
    if created:
        print(f"Created test student: {student.firstName} {student.lastName}")
    else:
        print(f"Using existing test student: {student.firstName} {student.lastName}")
    
    # Get or create a test professor
    professor, created = ProfessorProfile.objects.get_or_create(
        name='Dr. Test Professor',
        defaults={
            'title': 'Assistant Professor',
            'department': 'Computer Science',
            'institution': 'Test University',
            'researchAreas': ['Machine Learning', 'Artificial Intelligence'],
            'researchDescription': 'Research in machine learning and AI',
            'methods': ['Python', 'Deep Learning'],
            'acceptingStudents': True,
            'preferredDegreeLevels': ['BS', 'MS'],
            'prerequisites': 'Basic programming skills'
        }
    )
    
    if created:
        print(f"Created test professor: {professor.name}")
    else:
        print(f"Using existing test professor: {professor.name}")
    
    # Test matching service
    matching_service = MatchingService()
    
    print(f"\nStudent matching status before: {student.matchingStatus}")
    print(f"Student matching progress before: {student.matchingProgress}%")
    
    # Start matching
    success = matching_service.start_matching_for_student(str(student.id))
    
    if success:
        print("Matching process started successfully!")
        
        # Wait a bit for the background process
        import time
        time.sleep(2)
        
        # Check status
        status = matching_service.get_matching_status(str(student.id))
        print(f"Matching status: {status['status']}")
        print(f"Matching progress: {status['progress']}%")
        
        # Check if matches were created
        matches = Match.objects.filter(student=student)
        print(f"Number of matches created: {matches.count()}")
        
        for match in matches:
            print(f"Match with {match.professor.name}: Score {round(match.score, 2)}%, AI Score {round(match.aiScore, 2) if match.aiScore else 'N/A'}%")
            print(f"Highlights: {match.highlights}")
            print(f"AI Explanation: {match.aiExplanation[:100]}...")
            print("---")
    
    else:
        print("Failed to start matching process")

if __name__ == '__main__':
    test_matching_service()
