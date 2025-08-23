from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import StudentProfile, ProfessorProfile, ResearchProject
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
                'methods': ['Control Theory', 'Optimization'],
                'domains': ['Electrical Engineering', 'Robotics'],
                'programmingSkills': [
                    {'name': 'MATLAB', 'level': 5},
                    {'name': 'Python', 'level': 4},
                    {'name': 'C++', 'level': 3}
                ],
                'labSkills': ['Circuit Design', 'System Modeling'],
                'statisticalSkills': ['Time Series Analysis', 'Signal Processing'],
                'publications': [
                    {
                        'title': 'Robotic Control Systems: A Survey',
                        'venue': 'IEEE Robotics and Automation',
                        'year': 2023
                    }
                ],
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
                'researchAreas': ['Machine Learning', 'Computer Vision', 'Natural Language Processing'],
                'researchDescription': 'My research focuses on developing novel machine learning algorithms for computer vision and natural language processing applications.',
                'methods': ['Deep Learning', 'Computer Vision', 'NLP'],
                'publications': [
                    {
                        'title': 'Advances in Deep Learning for Computer Vision',
                        'venue': 'Nature Machine Intelligence',
                        'year': 2023
                    }
                ],
                'labWebsite': 'https://wilsonlab.stanford.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=wilson',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Strong background in machine learning and programming',
                'contactPreferences': ['in-app', 'email'],
                'profileCompleteness': 95
            }
        )
        
        professor2, created = ProfessorProfile.objects.get_or_create(
            user=user4,
            defaults={
                'name': 'Dr. Michael Chen',
                'title': 'Assistant Professor',
                'department': 'Electrical Engineering',
                'institution': 'MIT',
                'researchAreas': ['Robotics', 'Control Systems', 'Signal Processing'],
                'researchDescription': 'My research explores advanced control systems and robotics applications, with a focus on autonomous systems.',
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
        
        # Create sample research projects
        project1, created = ResearchProject.objects.get_or_create(
            title='Computer Vision for Autonomous Driving',
            defaults={
                'professor': professor1,
                'summary': 'Develop computer vision algorithms for autonomous vehicle navigation and safety systems.',
                'description': 'This project focuses on developing advanced computer vision algorithms that can be used in autonomous driving systems. Students will work on object detection, lane detection, and traffic sign recognition using deep learning techniques.',
                'researchAreas': ['Computer Vision', 'Machine Learning', 'Autonomous Systems'],
                'techniques': ['Deep Learning', 'Computer Vision', 'Object Detection'],
                'datasets': ['KITTI', 'Cityscapes', 'BDD100K'],
                'tools': ['PyTorch', 'OpenCV', 'TensorFlow'],
                'desiredSkills': [
                    {'name': 'Python', 'level': 4},
                    {'name': 'Computer Vision', 'level': 3},
                    {'name': 'Deep Learning', 'level': 3}
                ],
                'hoursPerWeek': 20,
                'startWindow': '2024-01-15',
                'endWindow': '2024-05-15',
                'compensation': 'Stipend',
                'location': 'Hybrid',
                'isActive': True
            }
        )
        
        project2, created = ResearchProject.objects.get_or_create(
            title='Robotic Control Systems for Manufacturing',
            defaults={
                'professor': professor2,
                'summary': 'Design and implement control systems for industrial robotics applications.',
                'description': 'This project involves developing control algorithms for industrial robots used in manufacturing processes. Students will work on trajectory planning, motion control, and safety systems.',
                'researchAreas': ['Robotics', 'Control Systems', 'Manufacturing'],
                'techniques': ['Control Theory', 'Trajectory Planning', 'Motion Control'],
                'datasets': ['Industrial Robot Data'],
                'tools': ['MATLAB', 'ROS', 'Simulink'],
                'desiredSkills': [
                    {'name': 'MATLAB', 'level': 4},
                    {'name': 'Control Theory', 'level': 4},
                    {'name': 'Robotics', 'level': 3}
                ],
                'hoursPerWeek': 25,
                'startWindow': '2024-02-01',
                'endWindow': '2024-08-01',
                'compensation': 'Stipend',
                'location': 'On-site',
                'isActive': True
            }
        )
        
        project3, created = ResearchProject.objects.get_or_create(
            title='Natural Language Processing for Healthcare',
            defaults={
                'professor': professor1,
                'summary': 'Develop NLP systems for processing medical documents and patient records.',
                'description': 'This project focuses on applying natural language processing techniques to healthcare data. Students will work on text classification, information extraction, and medical document analysis.',
                'researchAreas': ['Natural Language Processing', 'Healthcare', 'Machine Learning'],
                'techniques': ['NLP', 'Text Classification', 'Information Extraction'],
                'datasets': ['MIMIC-III', 'PubMed'],
                'tools': ['Transformers', 'spaCy', 'Hugging Face'],
                'desiredSkills': [
                    {'name': 'Python', 'level': 4},
                    {'name': 'NLP', 'level': 3},
                    {'name': 'Machine Learning', 'level': 3}
                ],
                'hoursPerWeek': 15,
                'startWindow': '2024-03-01',
                'endWindow': '2024-06-30',
                'compensation': 'Credit',
                'location': 'Remote',
                'isActive': True
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {StudentProfile.objects.count()} student profiles\n'
                f'- {ProfessorProfile.objects.count()} professor profiles\n'
                f'- {ResearchProject.objects.count()} research projects'
            )
        )
