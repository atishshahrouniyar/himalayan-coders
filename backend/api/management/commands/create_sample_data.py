from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import StudentProfile, ProfessorProfile
import uuid

class Command(BaseCommand):
    help = 'Create sample data for testing the API'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        user1, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student1@example.com',
                'first_name': 'Alice',
                'last_name': 'Johnson'
            }
        )
        
        user2, created = User.objects.get_or_create(
            username='student2',
            defaults={
                'email': 'student2@example.com',
                'first_name': 'Bob',
                'last_name': 'Smith'
            }
        )
        
        user3, created = User.objects.get_or_create(
            username='professor1',
            defaults={
                'email': 'professor1@university.edu',
                'first_name': 'Dr. Sarah',
                'last_name': 'Wilson'
            }
        )
        
        user4, created = User.objects.get_or_create(
            username='professor2',
            defaults={
                'email': 'professor2@university.edu',
                'first_name': 'Dr. Michael',
                'last_name': 'Chen'
            }
        )
        
        # Create sample student profiles
        student1, created = StudentProfile.objects.get_or_create(
            user=user1,
            defaults={
                'firstName': 'Alice',
                'lastName': 'Johnson',
                'email': 'student1@example.com',
                'university': 'Stanford University',
                'department': 'Computer Science',
                'degreeLevel': 'MS',
                'year': 2024,
                'semester': 1,
                'primaryInterests': ['Machine Learning', 'Computer Vision', 'Natural Language Processing'],
                'methods': ['Deep Learning', 'Statistical Analysis'],
                'domains': ['Computer Science', 'Artificial Intelligence'],
                'programmingSkills': [
                    {'name': 'Python', 'level': 4},
                    {'name': 'TensorFlow', 'level': 3},
                    {'name': 'PyTorch', 'level': 3}
                ],
                'labSkills': ['Data Analysis', 'Model Training'],
                'statisticalSkills': ['Regression Analysis', 'Hypothesis Testing'],
                'publications': [],
                'projects': [
                    {
                        'title': 'Image Classification with CNN',
                        'description': 'Built a convolutional neural network for image classification',
                        'role': 'Lead Developer'
                    }
                ],
                'workHistory': [],
                'coursework': ['Machine Learning', 'Computer Vision', 'Statistics'],
                'hoursPerWeek': 20,
                'startDate': '2024-01-15',
                'duration': 'Semester',
                'compensation': 'Credit',
                'creditSeeking': True,
                'profileVisibility': 'public',
                'profileCompleteness': 85
            }
        )
        
        student2, created = StudentProfile.objects.get_or_create(
            user=user2,
            defaults={
                'firstName': 'Bob',
                'lastName': 'Smith',
                'email': 'student2@example.com',
                'university': 'MIT',
                'department': 'Electrical Engineering',
                'degreeLevel': 'PhD',
                'year': 2024,
                'semester': 1,
                'primaryInterests': ['Robotics', 'Control Systems', 'Signal Processing'],
                'methods': ['Control Theory', 'Optimization', 'System Design'],
                'domains': ['Electrical Engineering', 'Robotics'],
                'programmingSkills': [
                    {'name': 'MATLAB', 'level': 5},
                    {'name': 'Python', 'level': 3},
                    {'name': 'C++', 'level': 4}
                ],
                'labSkills': ['Circuit Design', 'System Integration'],
                'statisticalSkills': ['Signal Processing', 'Time Series Analysis'],
                'publications': [],
                'projects': [
                    {
                        'title': 'Autonomous Robot Navigation',
                        'description': 'Developed navigation algorithms for autonomous robots',
                        'role': 'Research Assistant'
                    }
                ],
                'workHistory': [],
                'coursework': ['Control Systems', 'Robotics', 'Signal Processing'],
                'hoursPerWeek': 25,
                'startDate': '2024-02-01',
                'duration': 'Ongoing',
                'compensation': 'Stipend',
                'creditSeeking': False,
                'profileVisibility': 'public',
                'profileCompleteness': 90
            }
        )
        
        # Create sample professor profiles
        professor1, created = ProfessorProfile.objects.get_or_create(
            user=user3,
            defaults={
                'name': 'Dr. Sarah Wilson',
                'title': 'Associate Professor',
                'department': 'Computer Science',
                'institution': 'Stanford University',
                'researchAreas': ['Computer Vision', 'Machine Learning', 'Natural Language Processing'],
                'researchDescription': 'My research focuses on developing computer vision and machine learning algorithms for real-world applications.',
                'methods': ['Deep Learning', 'Computer Vision', 'Natural Language Processing'],
                'publications': [
                    {
                        'title': 'Advanced Computer Vision Techniques for Autonomous Systems',
                        'venue': 'CVPR',
                        'year': 2023
                    }
                ],
                'labWebsite': 'https://wilsonlab.stanford.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=wilson',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Strong background in computer science and mathematics',
                'contactPreferences': ['email'],
                'profileCompleteness': 95
            }
        )
        
        professor2, created = ProfessorProfile.objects.get_or_create(
            user=user4,
            defaults={
                'name': 'Dr. Michael Chen',
                'title': 'Professor',
                'department': 'Electrical Engineering',
                'institution': 'MIT',
                'researchAreas': ['Robotics', 'Control Systems', 'Autonomous Systems'],
                'researchDescription': 'My research focuses on control systems and robotics for autonomous applications.',
                'methods': ['Control Theory', 'Robotics', 'Optimization'],
                'publications': [
                    {
                        'title': 'Novel Control Algorithms for Autonomous Robots',
                        'venue': 'IEEE Transactions on Robotics',
                        'year': 2023
                    }
                ],
                'labWebsite': 'https://chenlab.mit.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=chen',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['PhD'],
                'prerequisites': 'Background in control theory and robotics',
                'contactPreferences': ['email'],
                'profileCompleteness': 90
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {StudentProfile.objects.count()} student profiles\n'
                f'- {ProfessorProfile.objects.count()} professor profiles'
            )
        )
