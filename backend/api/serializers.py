from rest_framework import serializers
from .models import StudentProfile, ProfessorProfile, Match
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ['id', 'createdAt', 'updatedAt', 'profileCompleteness']

class ProfessorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ProfessorProfile
        fields = '__all__'
        read_only_fields = ['id', 'createdAt', 'updatedAt', 'profileCompleteness']

class MatchSerializer(serializers.ModelSerializer):
    student = StudentProfileSerializer(read_only=True)
    professor = ProfessorProfileSerializer(read_only=True)
    
    class Meta:
        model = Match
        fields = '__all__'
        read_only_fields = ['id', 'createdAt', 'aiScore', 'aiExplanation', 'aiAnalysis', 'detailedScores']

# Simplified serializers for list views
class StudentProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'firstName', 'lastName', 'university', 'department', 'degreeLevel', 'primaryInterests', 'profileCompleteness']

class ProfessorProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorProfile
        fields = ['id', 'name', 'title', 'institution', 'department', 'researchAreas', 'acceptingStudents', 'profileCompleteness']
