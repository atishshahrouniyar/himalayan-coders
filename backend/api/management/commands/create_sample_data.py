from django.core.management.base import BaseCommand
from api.models import StudentProfile, ProfessorProfile
import uuid
import random

class Command(BaseCommand):
    help = 'Create comprehensive sample data for testing the API'

    def handle(self, *args, **options):
        self.stdout.write('Creating comprehensive sample data...')
        
        # Clear existing data
        ProfessorProfile.objects.all().delete()
        StudentProfile.objects.all().delete()
        
        # Create 30 diverse professors
        professors_data = [
            # Computer Science & AI
            {
                'name': 'Dr. Sarah Chen',
                'title': 'Associate Professor',
                'department': 'Computer Science',
                'institution': 'Stanford University',
                'researchAreas': ['Machine Learning', 'Computer Vision', 'Natural Language Processing'],
                'researchDescription': 'My research focuses on developing advanced machine learning algorithms for computer vision and natural language processing applications, with particular emphasis on deep learning and neural networks.',
                'methods': ['Deep Learning', 'Computer Vision', 'Neural Networks', 'Statistical Analysis'],
                'publications': [
                    {'title': 'Advanced Computer Vision Techniques for Autonomous Systems', 'venue': 'CVPR', 'year': 2023},
                    {'title': 'Neural Network Architectures for Natural Language Understanding', 'venue': 'ACL', 'year': 2022}
                ],
                'labWebsite': 'https://chenlab.stanford.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=chen_sarah',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Strong background in computer science, mathematics, and programming. Experience with Python, PyTorch, and machine learning frameworks.',
                'contactPreferences': ['email', 'office_hours'],
                'profileCompleteness': 95
            },
            {
                'name': 'Dr. Michael Rodriguez',
                'title': 'Professor',
                'department': 'Computer Science',
                'institution': 'MIT',
                'researchAreas': ['Artificial Intelligence', 'Robotics', 'Human-Computer Interaction'],
                'researchDescription': 'I lead research in artificial intelligence and robotics, focusing on human-robot interaction and autonomous systems that can work safely alongside humans.',
                'methods': ['Robotics', 'AI', 'Human-Computer Interaction', 'Control Systems'],
                'publications': [
                    {'title': 'Human-Robot Collaboration in Manufacturing Environments', 'venue': 'Science Robotics', 'year': 2023},
                    {'title': 'Autonomous Navigation for Service Robots', 'venue': 'IJRR', 'year': 2022}
                ],
                'labWebsite': 'https://rodriguezlab.mit.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=rodriguez_mike',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['PhD'],
                'prerequisites': 'Background in robotics, computer science, or mechanical engineering. Programming skills in Python, C++, and ROS.',
                'contactPreferences': ['email'],
                'profileCompleteness': 90
            },
            {
                'name': 'Dr. Emily Zhang',
                'title': 'Assistant Professor',
                'department': 'Computer Science',
                'institution': 'UC Berkeley',
                'researchAreas': ['Data Science', 'Big Data Analytics', 'Database Systems'],
                'researchDescription': 'My research focuses on scalable data processing systems, big data analytics, and database optimization for large-scale applications.',
                'methods': ['Data Mining', 'Database Systems', 'Distributed Computing', 'Statistical Analysis'],
                'publications': [
                    {'title': 'Scalable Data Processing for Real-time Analytics', 'venue': 'SIGMOD', 'year': 2023},
                    {'title': 'Optimization Techniques for Large-scale Databases', 'venue': 'VLDB', 'year': 2022}
                ],
                'labWebsite': 'https://zhanglab.berkeley.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=zhang_emily',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Strong programming skills, database knowledge, and experience with distributed systems.',
                'contactPreferences': ['email', 'slack'],
                'profileCompleteness': 88
            },
            
            # Engineering
            {
                'name': 'Dr. James Thompson',
                'title': 'Professor',
                'department': 'Electrical Engineering',
                'institution': 'Georgia Tech',
                'researchAreas': ['Power Systems', 'Renewable Energy', 'Smart Grid'],
                'researchDescription': 'My research focuses on power systems engineering, renewable energy integration, and smart grid technologies for sustainable energy solutions.',
                'methods': ['Power Systems Analysis', 'Control Theory', 'Optimization', 'Simulation'],
                'publications': [
                    {'title': 'Smart Grid Integration of Renewable Energy Sources', 'venue': 'IEEE Transactions on Power Systems', 'year': 2023},
                    {'title': 'Advanced Control Strategies for Power Distribution Networks', 'venue': 'IEEE PES', 'year': 2022}
                ],
                'labWebsite': 'https://thompsonlab.gatech.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=thompson_james',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in electrical engineering, power systems, or control theory. Experience with MATLAB and Simulink.',
                'contactPreferences': ['email', 'office_hours'],
                'profileCompleteness': 92
            },
            {
                'name': 'Dr. Lisa Park',
                'title': 'Associate Professor',
                'department': 'Mechanical Engineering',
                'institution': 'University of Michigan',
                'researchAreas': ['Biomechanics', 'Medical Devices', 'Tissue Engineering'],
                'researchDescription': 'I work on biomechanical engineering, developing medical devices and tissue engineering solutions for healthcare applications.',
                'methods': ['Biomechanics', 'Medical Device Design', 'Tissue Engineering', 'Biomaterials'],
                'publications': [
                    {'title': 'Novel Biomaterials for Tissue Regeneration', 'venue': 'Nature Materials', 'year': 2023},
                    {'title': 'Biomechanical Analysis of Joint Replacement Systems', 'venue': 'Journal of Biomechanics', 'year': 2022}
                ],
                'labWebsite': 'https://parklab.umich.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=park_lisa',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in mechanical engineering, biology, or biomedical engineering. Experience with CAD software and laboratory techniques.',
                'contactPreferences': ['email'],
                'profileCompleteness': 87
            },
            
            # Physics & Chemistry
            {
                'name': 'Dr. Robert Kim',
                'title': 'Professor',
                'department': 'Physics',
                'institution': 'Caltech',
                'researchAreas': ['Quantum Computing', 'Quantum Mechanics', 'Condensed Matter Physics'],
                'researchDescription': 'My research focuses on quantum computing, quantum mechanics, and condensed matter physics, particularly in developing quantum algorithms and quantum materials.',
                'methods': ['Quantum Mechanics', 'Quantum Computing', 'Condensed Matter Physics', 'Theoretical Physics'],
                'publications': [
                    {'title': 'Quantum Algorithms for Optimization Problems', 'venue': 'Nature Physics', 'year': 2023},
                    {'title': 'Novel Quantum Materials for Computing Applications', 'venue': 'Physical Review Letters', 'year': 2022}
                ],
                'labWebsite': 'https://kimlab.caltech.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=kim_robert',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['PhD'],
                'prerequisites': 'Strong background in physics, mathematics, and quantum mechanics. Programming skills in Python and quantum computing frameworks.',
                'contactPreferences': ['email'],
                'profileCompleteness': 94
            },
            {
                'name': 'Dr. Maria Garcia',
                'title': 'Associate Professor',
                'department': 'Chemistry',
                'institution': 'Harvard University',
                'researchAreas': ['Organic Chemistry', 'Drug Discovery', 'Chemical Biology'],
                'researchDescription': 'My research focuses on organic chemistry and drug discovery, developing new therapeutic compounds and understanding chemical biology mechanisms.',
                'methods': ['Organic Synthesis', 'Drug Discovery', 'Chemical Biology', 'Analytical Chemistry'],
                'publications': [
                    {'title': 'Novel Drug Candidates for Cancer Treatment', 'venue': 'Journal of Medicinal Chemistry', 'year': 2023},
                    {'title': 'Chemical Biology Approaches to Disease Understanding', 'venue': 'Nature Chemical Biology', 'year': 2022}
                ],
                'labWebsite': 'https://garciagroup.harvard.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=garcia_maria',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in chemistry, biochemistry, or chemical biology. Laboratory experience and knowledge of analytical techniques.',
                'contactPreferences': ['email', 'lab_meetings'],
                'profileCompleteness': 89
            },
            
            # Biology & Medicine
            {
                'name': 'Dr. David Wilson',
                'title': 'Professor',
                'department': 'Biology',
                'institution': 'Johns Hopkins University',
                'researchAreas': ['Genomics', 'Bioinformatics', 'Evolutionary Biology'],
                'researchDescription': 'My research focuses on genomics, bioinformatics, and evolutionary biology, studying genetic diversity and evolutionary processes.',
                'methods': ['Genomics', 'Bioinformatics', 'Evolutionary Biology', 'Statistical Genetics'],
                'publications': [
                    {'title': 'Genomic Analysis of Human Population Diversity', 'venue': 'Nature Genetics', 'year': 2023},
                    {'title': 'Evolutionary Patterns in Microbial Communities', 'venue': 'Science', 'year': 2022}
                ],
                'labWebsite': 'https://wilsonlab.jhu.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=wilson_david',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in biology, genetics, or bioinformatics. Programming skills in Python, R, and experience with genomic data analysis.',
                'contactPreferences': ['email'],
                'profileCompleteness': 91
            },
            {
                'name': 'Dr. Jennifer Lee',
                'title': 'Assistant Professor',
                'department': 'Neuroscience',
                'institution': 'UCLA',
                'researchAreas': ['Neuroscience', 'Brain Imaging', 'Cognitive Science'],
                'researchDescription': 'My research focuses on neuroscience and brain imaging, studying cognitive processes and neural mechanisms underlying human behavior.',
                'methods': ['Brain Imaging', 'Cognitive Science', 'Neuroscience', 'Statistical Analysis'],
                'publications': [
                    {'title': 'Neural Correlates of Decision Making Processes', 'venue': 'Nature Neuroscience', 'year': 2023},
                    {'title': 'Brain Imaging Techniques for Cognitive Assessment', 'venue': 'Journal of Neuroscience', 'year': 2022}
                ],
                'labWebsite': 'https://leelab.ucla.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=lee_jennifer',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in neuroscience, psychology, or cognitive science. Experience with brain imaging techniques and statistical analysis.',
                'contactPreferences': ['email', 'lab_meetings'],
                'profileCompleteness': 86
            },
            
            # Mathematics & Statistics
            {
                'name': 'Dr. Alexander Brown',
                'title': 'Professor',
                'department': 'Mathematics',
                'institution': 'Princeton University',
                'researchAreas': ['Applied Mathematics', 'Mathematical Modeling', 'Optimization'],
                'researchDescription': 'My research focuses on applied mathematics and mathematical modeling, developing mathematical frameworks for complex systems and optimization problems.',
                'methods': ['Mathematical Modeling', 'Optimization', 'Numerical Analysis', 'Applied Mathematics'],
                'publications': [
                    {'title': 'Mathematical Models for Complex Biological Systems', 'venue': 'SIAM Journal on Applied Mathematics', 'year': 2023},
                    {'title': 'Optimization Algorithms for Large-scale Problems', 'venue': 'Mathematical Programming', 'year': 2022}
                ],
                'labWebsite': 'https://brownlab.princeton.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=brown_alex',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Strong mathematical background, programming skills in MATLAB or Python, and experience with mathematical modeling.',
                'contactPreferences': ['email'],
                'profileCompleteness': 93
            },
            {
                'name': 'Dr. Rachel Green',
                'title': 'Associate Professor',
                'department': 'Statistics',
                'institution': 'University of Washington',
                'researchAreas': ['Statistical Learning', 'Data Science', 'Biostatistics'],
                'researchDescription': 'My research focuses on statistical learning, data science, and biostatistics, developing statistical methods for complex data analysis.',
                'methods': ['Statistical Learning', 'Data Science', 'Biostatistics', 'Machine Learning'],
                'publications': [
                    {'title': 'Statistical Methods for High-dimensional Data Analysis', 'venue': 'Journal of the American Statistical Association', 'year': 2023},
                    {'title': 'Machine Learning Approaches in Biostatistics', 'venue': 'Biometrics', 'year': 2022}
                ],
                'labWebsite': 'https://greenlab.uw.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=green_rachel',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Strong statistical background, programming skills in R and Python, and experience with data analysis.',
                'contactPreferences': ['email', 'office_hours'],
                'profileCompleteness': 90
            },
            
            # Environmental Science
            {
                'name': 'Dr. Thomas Anderson',
                'title': 'Professor',
                'department': 'Environmental Science',
                'institution': 'UC Santa Barbara',
                'researchAreas': ['Climate Change', 'Environmental Modeling', 'Sustainability'],
                'researchDescription': 'My research focuses on climate change, environmental modeling, and sustainability, studying environmental systems and developing solutions for environmental challenges.',
                'methods': ['Environmental Modeling', 'Climate Science', 'Sustainability Analysis', 'Geographic Information Systems'],
                'publications': [
                    {'title': 'Climate Change Impacts on Coastal Ecosystems', 'venue': 'Nature Climate Change', 'year': 2023},
                    {'title': 'Environmental Modeling for Sustainability Planning', 'venue': 'Environmental Science & Technology', 'year': 2022}
                ],
                'labWebsite': 'https://andersonlab.ucsb.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=anderson_thomas',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in environmental science, ecology, or related fields. Experience with environmental modeling and GIS software.',
                'contactPreferences': ['email'],
                'profileCompleteness': 88
            },
            
            # Materials Science
            {
                'name': 'Dr. Sophia Martinez',
                'title': 'Assistant Professor',
                'department': 'Materials Science',
                'institution': 'Northwestern University',
                'researchAreas': ['Nanomaterials', 'Energy Storage', 'Materials Characterization'],
                'researchDescription': 'My research focuses on nanomaterials, energy storage, and materials characterization, developing new materials for energy applications.',
                'methods': ['Materials Synthesis', 'Characterization Techniques', 'Energy Storage', 'Nanotechnology'],
                'publications': [
                    {'title': 'Novel Nanomaterials for Energy Storage Applications', 'venue': 'Advanced Materials', 'year': 2023},
                    {'title': 'Characterization Techniques for Nanomaterials', 'venue': 'Nature Materials', 'year': 2022}
                ],
                'labWebsite': 'https://martinezlab.northwestern.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=martinez_sophia',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in materials science, chemistry, or physics. Experience with materials characterization techniques and laboratory work.',
                'contactPreferences': ['email', 'lab_meetings'],
                'profileCompleteness': 87
            },
            
            # Economics & Social Sciences
            {
                'name': 'Dr. Christopher Taylor',
                'title': 'Professor',
                'department': 'Economics',
                'institution': 'University of Chicago',
                'researchAreas': ['Behavioral Economics', 'Experimental Economics', 'Game Theory'],
                'researchDescription': 'My research focuses on behavioral economics, experimental economics, and game theory, studying human decision-making and economic behavior.',
                'methods': ['Experimental Economics', 'Behavioral Economics', 'Game Theory', 'Statistical Analysis'],
                'publications': [
                    {'title': 'Behavioral Patterns in Economic Decision Making', 'venue': 'American Economic Review', 'year': 2023},
                    {'title': 'Experimental Approaches to Game Theory', 'venue': 'Econometrica', 'year': 2022}
                ],
                'labWebsite': 'https://taylorlab.uchicago.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=taylor_chris',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Strong background in economics, mathematics, and statistics. Experience with experimental design and statistical analysis.',
                'contactPreferences': ['email', 'office_hours'],
                'profileCompleteness': 92
            },
            {
                'name': 'Dr. Amanda White',
                'title': 'Associate Professor',
                'department': 'Psychology',
                'institution': 'Yale University',
                'researchAreas': ['Social Psychology', 'Cognitive Psychology', 'Human Development'],
                'researchDescription': 'My research focuses on social psychology, cognitive psychology, and human development, studying psychological processes and human behavior.',
                'methods': ['Social Psychology', 'Cognitive Psychology', 'Human Development', 'Experimental Design'],
                'publications': [
                    {'title': 'Social Influences on Cognitive Development', 'venue': 'Psychological Science', 'year': 2023},
                    {'title': 'Cognitive Processes in Social Interactions', 'venue': 'Journal of Experimental Psychology', 'year': 2022}
                ],
                'labWebsite': 'https://whitelab.yale.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=white_amanda',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in psychology, cognitive science, or related fields. Experience with experimental design and statistical analysis.',
                'contactPreferences': ['email'],
                'profileCompleteness': 89
            },
            
            # More diverse professors
            {
                'name': 'Dr. Kevin Patel',
                'title': 'Assistant Professor',
                'department': 'Computer Engineering',
                'institution': 'Carnegie Mellon University',
                'researchAreas': ['Embedded Systems', 'IoT', 'Hardware Security'],
                'researchDescription': 'My research focuses on embedded systems, Internet of Things (IoT), and hardware security, developing secure and efficient embedded computing solutions.',
                'methods': ['Embedded Systems', 'IoT', 'Hardware Security', 'VLSI Design'],
                'publications': [
                    {'title': 'Security Protocols for IoT Devices', 'venue': 'IEEE Security & Privacy', 'year': 2023},
                    {'title': 'Energy-efficient Embedded Systems Design', 'venue': 'IEEE Transactions on Computers', 'year': 2022}
                ],
                'labWebsite': 'https://patellab.cmu.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=patel_kevin',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in computer engineering, electrical engineering, or computer science. Experience with embedded systems and hardware design.',
                'contactPreferences': ['email', 'slack'],
                'profileCompleteness': 85
            },
            {
                'name': 'Dr. Nicole Johnson',
                'title': 'Professor',
                'department': 'Chemical Engineering',
                'institution': 'University of Texas at Austin',
                'researchAreas': ['Process Engineering', 'Catalysis', 'Reaction Engineering'],
                'researchDescription': 'My research focuses on process engineering, catalysis, and reaction engineering, developing efficient chemical processes and catalytic systems.',
                'methods': ['Process Engineering', 'Catalysis', 'Reaction Engineering', 'Chemical Kinetics'],
                'publications': [
                    {'title': 'Novel Catalytic Processes for Sustainable Chemistry', 'venue': 'Chemical Engineering Science', 'year': 2023},
                    {'title': 'Reaction Engineering for Green Chemistry', 'venue': 'AIChE Journal', 'year': 2022}
                ],
                'labWebsite': 'https://johnsonlab.utexas.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=johnson_nicole',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in chemical engineering, chemistry, or related fields. Experience with process design and laboratory techniques.',
                'contactPreferences': ['email', 'lab_meetings'],
                'profileCompleteness': 91
            },
            {
                'name': 'Dr. Daniel Kim',
                'title': 'Associate Professor',
                'department': 'Aerospace Engineering',
                'institution': 'University of Illinois Urbana-Champaign',
                'researchAreas': ['Aerodynamics', 'Flight Dynamics', 'Space Systems'],
                'researchDescription': 'My research focuses on aerodynamics, flight dynamics, and space systems, developing advanced aerospace technologies and systems.',
                'methods': ['Aerodynamics', 'Flight Dynamics', 'Space Systems', 'Computational Fluid Dynamics'],
                'publications': [
                    {'title': 'Advanced Aerodynamic Design for Aircraft', 'venue': 'AIAA Journal', 'year': 2023},
                    {'title': 'Flight Dynamics Analysis for Space Vehicles', 'venue': 'Journal of Spacecraft and Rockets', 'year': 2022}
                ],
                'labWebsite': 'https://kimlab.illinois.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=kim_daniel',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in aerospace engineering, mechanical engineering, or related fields. Experience with CFD software and aerospace systems.',
                'contactPreferences': ['email'],
                'profileCompleteness': 88
            },
            {
                'name': 'Dr. Laura Davis',
                'title': 'Assistant Professor',
                'department': 'Civil Engineering',
                'institution': 'University of California, Davis',
                'researchAreas': ['Structural Engineering', 'Earthquake Engineering', 'Infrastructure Systems'],
                'researchDescription': 'My research focuses on structural engineering, earthquake engineering, and infrastructure systems, developing resilient and sustainable infrastructure solutions.',
                'methods': ['Structural Engineering', 'Earthquake Engineering', 'Infrastructure Systems', 'Finite Element Analysis'],
                'publications': [
                    {'title': 'Seismic Design of Resilient Infrastructure Systems', 'venue': 'Earthquake Engineering & Structural Dynamics', 'year': 2023},
                    {'title': 'Sustainable Materials for Structural Applications', 'venue': 'Journal of Structural Engineering', 'year': 2022}
                ],
                'labWebsite': 'https://davislab.ucdavis.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=davis_laura',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in civil engineering, structural engineering, or related fields. Experience with structural analysis software and laboratory testing.',
                'contactPreferences': ['email', 'office_hours'],
                'profileCompleteness': 86
            },
            {
                'name': 'Dr. Ryan Thompson',
                'title': 'Professor',
                'department': 'Industrial Engineering',
                'institution': 'Purdue University',
                'researchAreas': ['Operations Research', 'Supply Chain Management', 'Manufacturing Systems'],
                'researchDescription': 'My research focuses on operations research, supply chain management, and manufacturing systems, optimizing complex industrial processes and systems.',
                'methods': ['Operations Research', 'Supply Chain Management', 'Manufacturing Systems', 'Optimization'],
                'publications': [
                    {'title': 'Optimization Models for Supply Chain Management', 'venue': 'Operations Research', 'year': 2023},
                    {'title': 'Manufacturing Systems Design and Analysis', 'venue': 'IIE Transactions', 'year': 2022}
                ],
                'labWebsite': 'https://thompsonlab.purdue.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=thompson_ryan',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in industrial engineering, operations research, or related fields. Experience with optimization software and mathematical modeling.',
                'contactPreferences': ['email'],
                'profileCompleteness': 90
            },
            {
                'name': 'Dr. Michelle Wong',
                'title': 'Associate Professor',
                'department': 'Biomedical Engineering',
                'institution': 'Duke University',
                'researchAreas': ['Medical Imaging', 'Biomedical Devices', 'Tissue Engineering'],
                'researchDescription': 'My research focuses on medical imaging, biomedical devices, and tissue engineering, developing technologies for healthcare applications.',
                'methods': ['Medical Imaging', 'Biomedical Devices', 'Tissue Engineering', 'Biomaterials'],
                'publications': [
                    {'title': 'Advanced Medical Imaging Techniques for Diagnosis', 'venue': 'IEEE Transactions on Medical Imaging', 'year': 2023},
                    {'title': 'Biomedical Devices for Patient Monitoring', 'venue': 'Annals of Biomedical Engineering', 'year': 2022}
                ],
                'labWebsite': 'https://wonglab.duke.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=wong_michelle',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in biomedical engineering, electrical engineering, or related fields. Experience with medical devices and imaging systems.',
                'contactPreferences': ['email', 'lab_meetings'],
                'profileCompleteness': 87
            },
            {
                'name': 'Dr. Andrew Clark',
                'title': 'Assistant Professor',
                'department': 'Nuclear Engineering',
                'institution': 'University of Wisconsin-Madison',
                'researchAreas': ['Nuclear Safety', 'Radiation Physics', 'Nuclear Materials'],
                'researchDescription': 'My research focuses on nuclear safety, radiation physics, and nuclear materials, developing safe and efficient nuclear technologies.',
                'methods': ['Nuclear Safety', 'Radiation Physics', 'Nuclear Materials', 'Monte Carlo Simulation'],
                'publications': [
                    {'title': 'Nuclear Safety Analysis for Advanced Reactors', 'venue': 'Nuclear Science and Engineering', 'year': 2023},
                    {'title': 'Radiation Physics in Nuclear Applications', 'venue': 'Health Physics', 'year': 2022}
                ],
                'labWebsite': 'https://clarklab.wisc.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=clark_andrew',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in nuclear engineering, physics, or related fields. Experience with radiation detection and nuclear safety analysis.',
                'contactPreferences': ['email'],
                'profileCompleteness': 84
            },
            {
                'name': 'Dr. Jessica Lee',
                'title': 'Professor',
                'department': 'Ocean Engineering',
                'institution': 'University of Rhode Island',
                'researchAreas': ['Ocean Acoustics', 'Marine Robotics', 'Coastal Engineering'],
                'researchDescription': 'My research focuses on ocean acoustics, marine robotics, and coastal engineering, developing technologies for ocean exploration and coastal protection.',
                'methods': ['Ocean Acoustics', 'Marine Robotics', 'Coastal Engineering', 'Underwater Systems'],
                'publications': [
                    {'title': 'Ocean Acoustic Communication Systems', 'venue': 'Journal of the Acoustical Society of America', 'year': 2023},
                    {'title': 'Marine Robotics for Ocean Exploration', 'venue': 'Ocean Engineering', 'year': 2022}
                ],
                'labWebsite': 'https://leelab.uri.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=lee_jessica',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in ocean engineering, mechanical engineering, or related fields. Experience with underwater systems and marine technology.',
                'contactPreferences': ['email', 'field_trips'],
                'profileCompleteness': 89
            },
            {
                'name': 'Dr. Robert Chen',
                'title': 'Associate Professor',
                'department': 'Systems Engineering',
                'institution': 'University of Virginia',
                'researchAreas': ['Systems Engineering', 'Model-Based Design', 'Complex Systems'],
                'researchDescription': 'My research focuses on systems engineering, model-based design, and complex systems, developing methodologies for designing and analyzing complex engineering systems.',
                'methods': ['Systems Engineering', 'Model-Based Design', 'Complex Systems', 'Systems Analysis'],
                'publications': [
                    {'title': 'Model-Based Design for Complex Engineering Systems', 'venue': 'Systems Engineering', 'year': 2023},
                    {'title': 'Systems Analysis for Large-scale Projects', 'venue': 'IEEE Systems Journal', 'year': 2022}
                ],
                'labWebsite': 'https://chenlab.virginia.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=chen_robert',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in systems engineering, industrial engineering, or related fields. Experience with systems modeling and analysis tools.',
                'contactPreferences': ['email', 'office_hours'],
                'profileCompleteness': 86
            },
            {
                'name': 'Dr. Stephanie Brown',
                'title': 'Assistant Professor',
                'department': 'Agricultural Engineering',
                'institution': 'Iowa State University',
                'researchAreas': ['Precision Agriculture', 'Agricultural Robotics', 'Food Safety'],
                'researchDescription': 'My research focuses on precision agriculture, agricultural robotics, and food safety, developing technologies for sustainable and efficient agricultural systems.',
                'methods': ['Precision Agriculture', 'Agricultural Robotics', 'Food Safety', 'Sensor Technology'],
                'publications': [
                    {'title': 'Robotic Systems for Precision Agriculture', 'venue': 'Computers and Electronics in Agriculture', 'year': 2023},
                    {'title': 'Sensor Technologies for Food Safety Monitoring', 'venue': 'Food Control', 'year': 2022}
                ],
                'labWebsite': 'https://brownlab.iastate.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=brown_stephanie',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in agricultural engineering, mechanical engineering, or related fields. Experience with robotics and sensor systems.',
                'contactPreferences': ['email', 'field_work'],
                'profileCompleteness': 85
            },
            {
                'name': 'Dr. Kevin Martinez',
                'title': 'Professor',
                'department': 'Mining Engineering',
                'institution': 'Colorado School of Mines',
                'researchAreas': ['Mining Safety', 'Mineral Processing', 'Mine Planning'],
                'researchDescription': 'My research focuses on mining safety, mineral processing, and mine planning, developing safe and efficient mining technologies and processes.',
                'methods': ['Mining Safety', 'Mineral Processing', 'Mine Planning', 'Geotechnical Engineering'],
                'publications': [
                    {'title': 'Safety Systems for Underground Mining Operations', 'venue': 'Mining Engineering', 'year': 2023},
                    {'title': 'Advanced Mineral Processing Techniques', 'venue': 'Minerals Engineering', 'year': 2022}
                ],
                'labWebsite': 'https://martinezlab.mines.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=martinez_kevin',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in mining engineering, geological engineering, or related fields. Experience with mining operations and safety systems.',
                'contactPreferences': ['email'],
                'profileCompleteness': 88
            },
            {
                'name': 'Dr. Lisa Anderson',
                'title': 'Associate Professor',
                'department': 'Petroleum Engineering',
                'institution': 'Texas A&M University',
                'researchAreas': ['Reservoir Engineering', 'Enhanced Oil Recovery', 'Unconventional Resources'],
                'researchDescription': 'My research focuses on reservoir engineering, enhanced oil recovery, and unconventional resources, developing technologies for efficient hydrocarbon extraction.',
                'methods': ['Reservoir Engineering', 'Enhanced Oil Recovery', 'Unconventional Resources', 'Reservoir Simulation'],
                'publications': [
                    {'title': 'Enhanced Oil Recovery Techniques for Unconventional Reservoirs', 'venue': 'SPE Journal', 'year': 2023},
                    {'title': 'Reservoir Simulation for Complex Geological Systems', 'venue': 'Journal of Petroleum Technology', 'year': 2022}
                ],
                'labWebsite': 'https://andersonlab.tamu.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=anderson_lisa',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in petroleum engineering, chemical engineering, or related fields. Experience with reservoir simulation and petroleum operations.',
                'contactPreferences': ['email', 'field_trips'],
                'profileCompleteness': 87
            },
            {
                'name': 'Dr. Michael Garcia',
                'title': 'Assistant Professor',
                'department': 'Textile Engineering',
                'institution': 'North Carolina State University',
                'researchAreas': ['Smart Textiles', 'Fiber Science', 'Textile Manufacturing'],
                'researchDescription': 'My research focuses on smart textiles, fiber science, and textile manufacturing, developing advanced textile materials and manufacturing processes.',
                'methods': ['Smart Textiles', 'Fiber Science', 'Textile Manufacturing', 'Materials Science'],
                'publications': [
                    {'title': 'Smart Textiles for Wearable Technology Applications', 'venue': 'Textile Research Journal', 'year': 2023},
                    {'title': 'Advanced Fiber Materials for Technical Applications', 'venue': 'Journal of Materials Science', 'year': 2022}
                ],
                'labWebsite': 'https://garciagroup.ncsu.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=garcia_michael',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in textile engineering, materials science, or related fields. Experience with textile manufacturing and materials characterization.',
                'contactPreferences': ['email', 'lab_meetings'],
                'profileCompleteness': 84
            },
            {
                'name': 'Dr. Sarah Johnson',
                'title': 'Professor',
                'department': 'Forestry Engineering',
                'institution': 'Oregon State University',
                'researchAreas': ['Forest Management', 'Wood Science', 'Sustainable Forestry'],
                'researchDescription': 'My research focuses on forest management, wood science, and sustainable forestry, developing sustainable forest management practices and wood products.',
                'methods': ['Forest Management', 'Wood Science', 'Sustainable Forestry', 'Remote Sensing'],
                'publications': [
                    {'title': 'Sustainable Forest Management Practices', 'venue': 'Forest Science', 'year': 2023},
                    {'title': 'Advanced Wood Products and Applications', 'venue': 'Wood and Fiber Science', 'year': 2022}
                ],
                'labWebsite': 'https://johnsonlab.oregonstate.edu',
                'googleScholarUrl': 'https://scholar.google.com/citations?user=johnson_sarah',
                'acceptingStudents': True,
                'preferredDegreeLevels': ['MS', 'PhD'],
                'prerequisites': 'Background in forestry engineering, environmental science, or related fields. Experience with forest management and wood science.',
                'contactPreferences': ['email', 'field_work'],
                'profileCompleteness': 86
            }
        ]
        
        # Create professors
        created_professors = []
        for prof_data in professors_data:
            professor = ProfessorProfile.objects.create(**prof_data)
            created_professors.append(professor)
            self.stdout.write(f'Created professor: {professor.name} - {professor.institution}')
        
        # Create some sample students for testing
        students_data = [
            {
                'firstName': 'Alice',
                'lastName': 'Johnson',
                'email': 'alice.johnson@stanford.edu',
                'university': 'Stanford University',
                'department': 'Computer Science',
                'degreeLevel': 'MS',
                'year': 2024,
                'semester': 1,
                'primaryInterests': ['Machine Learning', 'Computer Vision', 'Natural Language Processing'],
                'methods': ['Deep Learning', 'Statistical Analysis'],
                'programmingSkills': [
                    {'name': 'Python', 'level': 4},
                    {'name': 'TensorFlow', 'level': 3},
                    {'name': 'PyTorch', 'level': 3}
                ],
                'labSkills': ['Data Analysis', 'Model Training'],
                'statisticalSkills': ['Regression Analysis', 'Hypothesis Testing'],
                'hoursPerWeek': 20,
                'startDate': '2024-01-15',
                'duration': 'Semester',
                'compensation': 'Credit',
                'creditSeeking': True,
                'profileVisibility': 'public',
                'profileCompleteness': 85,
                'matchingStatus': 'pending'
            },
            {
                'firstName': 'Bob',
                'lastName': 'Smith',
                'email': 'bob.smith@mit.edu',
                'university': 'MIT',
                'department': 'Electrical Engineering',
                'degreeLevel': 'PhD',
                'year': 2024,
                'semester': 1,
                'primaryInterests': ['Robotics', 'Control Systems', 'Signal Processing'],
                'methods': ['Control Theory', 'Optimization', 'System Design'],
                'programmingSkills': [
                    {'name': 'MATLAB', 'level': 5},
                    {'name': 'Python', 'level': 3},
                    {'name': 'C++', 'level': 4}
                ],
                'labSkills': ['Circuit Design', 'System Integration'],
                'statisticalSkills': ['Signal Processing', 'Time Series Analysis'],
                'hoursPerWeek': 25,
                'startDate': '2024-02-01',
                'duration': 'Ongoing',
                'compensation': 'Stipend',
                'creditSeeking': False,
                'profileVisibility': 'public',
                'profileCompleteness': 90,
                'matchingStatus': 'pending'
            }
        ]
        
        # Create students
        created_students = []
        for student_data in students_data:
            student = StudentProfile.objects.create(**student_data)
            created_students.append(student)
            self.stdout.write(f'Created student: {student.firstName} {student.lastName} - {student.university}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created comprehensive sample data:\n'
                f'- {len(created_professors)} professor profiles with diverse backgrounds\n'
                f'- {len(created_students)} student profiles for testing\n'
                f'\nProfessors cover various fields including:\n'
                f'- Computer Science & AI (Machine Learning, Robotics, Data Science)\n'
                f'- Engineering (Electrical, Mechanical, Chemical, Civil, Aerospace)\n'
                f'- Sciences (Physics, Chemistry, Biology, Neuroscience)\n'
                f'- Mathematics & Statistics\n'
                f'- Environmental Science\n'
                f'- Materials Science\n'
                f'- Social Sciences (Economics, Psychology)\n'
                f'- Specialized Engineering (Nuclear, Ocean, Systems, Agricultural, Mining, Petroleum, Textile, Forestry)\n'
                f'\nAll professors have:\n'
                f'- Detailed research descriptions\n'
                f'- Recent publications\n'
                f'- Specific prerequisites and requirements\n'
                f'- Various contact preferences\n'
                f'- Different academic ranks and institutions'
            )
        )
