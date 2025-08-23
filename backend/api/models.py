from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import uuid

class StudentProfile(models.Model):
    DEGREE_CHOICES = [
        ('BS', 'Bachelor of Science'),
        ('MS', 'Master of Science'),
        ('PhD', 'Doctor of Philosophy'),
        ('Other', 'Other'),
    ]
    
    REMOTE_CHOICES = [
        ('On-site', 'On-site'),
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('invite-only', 'Invite Only'),
        ('private', 'Private'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    preferredName = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    university = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    degreeLevel = models.CharField(max_length=10, choices=DEGREE_CHOICES)
    year = models.IntegerField()
    semester = models.IntegerField()
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    graduationTarget = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    remotePreference = models.CharField(max_length=10, choices=REMOTE_CHOICES, blank=True, null=True)
    workAuthorization = models.CharField(max_length=200, blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)
    
    # Research Interests
    primaryInterests = ArrayField(models.CharField(max_length=100), default=list)
    methods = ArrayField(models.CharField(max_length=100), default=list)
    domains = ArrayField(models.CharField(max_length=100), default=list)
    interestStatement = models.TextField(blank=True, null=True)
    
    # Skills
    programmingSkills = models.JSONField(default=list)  # Will store Skill objects
    labSkills = ArrayField(models.CharField(max_length=100), default=list)
    statisticalSkills = ArrayField(models.CharField(max_length=100), default=list)
    
    # Experience
    publications = models.JSONField(default=list)  # Will store Publication objects
    projects = models.JSONField(default=list)  # Will store Project objects
    workHistory = models.JSONField(default=list)  # Will store WorkRole objects
    coursework = ArrayField(models.CharField(max_length=200), default=list)
    
    # Availability
    hoursPerWeek = models.IntegerField()
    startDate = models.DateField(blank=True, null=True)
    duration = models.CharField(max_length=20, blank=True, null=True)
    compensation = models.CharField(max_length=20, blank=True, null=True)
    creditSeeking = models.BooleanField(default=False)
    
    # Documents & Links
    cvUrl = models.URLField(blank=True, null=True)
    portfolioUrl = models.URLField(blank=True, null=True)
    googleScholarUrl = models.URLField(blank=True, null=True)
    orcidUrl = models.URLField(blank=True, null=True)
    githubUrl = models.URLField(blank=True, null=True)
    linkedinUrl = models.URLField(blank=True, null=True)
    
    # Privacy
    profileVisibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='public')
    
    # Metadata
    profileCompleteness = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'student_profiles'
    
    def __str__(self):
        return f"{self.firstName} {self.lastName} - {self.university}"

class ProfessorProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='professor_profile')
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    researchAreas = ArrayField(models.CharField(max_length=100), default=list)
    researchDescription = models.TextField(blank=True, null=True)
    methods = ArrayField(models.CharField(max_length=100), default=list)
    publications = models.JSONField(default=list)  # Will store Publication objects
    labWebsite = models.URLField(blank=True, null=True)
    googleScholarUrl = models.URLField(blank=True, null=True)
    orcidUrl = models.URLField(blank=True, null=True)
    acceptingStudents = models.BooleanField(default=True)
    preferredDegreeLevels = ArrayField(models.CharField(max_length=10), default=list)
    prerequisites = models.TextField(blank=True, null=True)
    contactPreferences = ArrayField(models.CharField(max_length=20), default=list)
    
    # Metadata
    profileCompleteness = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'professor_profiles'
    
    def __str__(self):
        return f"Dr. {self.name} - {self.institution}"

class Match(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='matches')
    professor = models.ForeignKey(ProfessorProfile, on_delete=models.CASCADE, related_name='matches')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    highlights = ArrayField(models.CharField(max_length=200), default=list)
    studentInterests = ArrayField(models.CharField(max_length=100), default=list)
    professorInterests = ArrayField(models.CharField(max_length=100), default=list)
    skillFit = models.JSONField(default=list)  # Will store SkillFit objects
    availabilityFit = models.BooleanField(default=False)
    levelFit = models.BooleanField(default=False)
    
    # AI-enhanced fields
    aiScore = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    aiExplanation = models.TextField(blank=True, null=True)
    aiAnalysis = models.JSONField(default=dict)  # Store detailed AI analysis
    detailedScores = models.JSONField(default=dict)  # Store individual score breakdowns
    
    createdAt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'matches'
    
    def __str__(self):
        return f"Match: {self.student.firstName} {self.student.lastName} - {self.professor.name}"
