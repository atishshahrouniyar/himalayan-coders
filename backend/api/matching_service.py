import asyncio
import threading
from datetime import datetime
from typing import List, Dict, Any
from django.utils import timezone
from .models import StudentProfile, ProfessorProfile, Match
from .gemini_service import GeminiMatchingService

class MatchingService:
    def __init__(self):
        self.gemini_service = GeminiMatchingService()
    
    def start_matching_for_student(self, student_id: str) -> bool:
        """
        Start the matching process for a student in a background thread
        """
        try:
            student = StudentProfile.objects.get(id=student_id)
            
            # Update status to in progress
            student.matchingStatus = 'in_progress'
            student.matchingProgress = 0
            student.matchingStartedAt = timezone.now()
            student.matchingError = None
            student.save()
            
            # Start background thread
            thread = threading.Thread(
                target=self._run_matching_process,
                args=(student_id,),
                daemon=True
            )
            thread.start()
            
            return True
        except StudentProfile.DoesNotExist:
            return False
        except Exception as e:
            # Update status to failed
            try:
                student = StudentProfile.objects.get(id=student_id)
                student.matchingStatus = 'failed'
                student.matchingError = str(e)
                student.save()
            except:
                pass
            return False
    
    def _run_matching_process(self, student_id: str):
        """
        Run the matching process in background
        """
        try:
            student = StudentProfile.objects.get(id=student_id)
            professors = ProfessorProfile.objects.filter(acceptingStudents=True)
            total_professors = professors.count()
            
            if total_professors == 0:
                # No professors available
                student.matchingStatus = 'completed'
                student.matchingProgress = 100
                student.matchingCompletedAt = timezone.now()
                student.save()
                return
            
            # Calculate progress increment
            progress_increment = 100 / total_professors
            
            for i, professor in enumerate(professors):
                try:
                    # Check if match already exists
                    existing_match = Match.objects.filter(
                        student=student,
                        professor=professor
                    ).first()
                    
                    if existing_match:
                        # Update existing match with new analysis
                        self._update_match(existing_match, student, professor)
                    else:
                        # Create new match
                        self._create_match(student, professor)
                    
                    # Update progress
                    progress = min(100, int((i + 1) * progress_increment))
                    student.matchingProgress = progress
                    student.save()
                    
                except Exception as e:
                    print(f"Error matching student {student_id} with professor {professor.id}: {e}")
                    continue
            
            # Mark as completed
            student.matchingStatus = 'completed'
            student.matchingProgress = 100
            student.matchingCompletedAt = timezone.now()
            student.save()
            
        except Exception as e:
            # Mark as failed
            try:
                student = StudentProfile.objects.get(id=student_id)
                student.matchingStatus = 'failed'
                student.matchingError = str(e)
                student.save()
            except:
                pass
    
    def _create_match(self, student: StudentProfile, professor: ProfessorProfile):
        """
        Create a new match between student and professor
        """
        try:
            # Basic scoring
            score = self._calculate_basic_score(student, professor)
            
            # AI-enhanced analysis
            ai_score = None
            ai_explanation = ""
            ai_analysis = {}
            detailed_scores = {}
            
            try:
                ai_result = self.gemini_service.analyze_match(student.__dict__, professor.__dict__)
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
                score=round(score, 2),
                aiScore=round(ai_score, 2) if ai_score is not None else None,
                aiExplanation=ai_explanation,
                aiAnalysis=ai_analysis,
                detailedScores=detailed_scores,
                highlights=self._generate_highlights(student, professor),
                studentInterests=student.primaryInterests,
                professorInterests=professor.researchAreas
            )
            
        except Exception as e:
            print(f"Error creating match: {e}")
            raise
    
    def _update_match(self, match: Match, student: StudentProfile, professor: ProfessorProfile):
        """
        Update an existing match with new analysis
        """
        try:
            # Recalculate basic score
            score = self._calculate_basic_score(student, professor)
            
            # Update AI analysis
            try:
                ai_result = self.gemini_service.analyze_match(student.__dict__, professor.__dict__)
                match.aiScore = round(ai_result.get('score', score), 2)
                match.aiExplanation = ai_result.get('explanation', '')
                match.aiAnalysis = ai_result.get('analysis', {})
                match.detailedScores = ai_result.get('detailed_scores', {})
            except Exception as e:
                print(f"AI analysis failed: {e}")
                match.aiScore = round(score, 2)
            
            # Update other fields
            match.score = round(score, 2)
            match.highlights = self._generate_highlights(student, professor)
            match.studentInterests = student.primaryInterests
            match.professorInterests = professor.researchAreas
            match.save()
            
        except Exception as e:
            print(f"Error updating match: {e}")
            raise
    
    def _calculate_basic_score(self, student: StudentProfile, professor: ProfessorProfile) -> float:
        """
        Calculate basic compatibility score
        """
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
        if student.hoursPerWeek and student.hoursPerWeek >= 10:
            score += 20
        
        return min(score, 100)
    
    def _generate_highlights(self, student: StudentProfile, professor: ProfessorProfile) -> List[str]:
        """
        Generate match highlights
        """
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
    
    def get_matching_status(self, student_id: str) -> Dict[str, Any]:
        """
        Get the current matching status for a student
        """
        try:
            student = StudentProfile.objects.get(id=student_id)
            return {
                'status': student.matchingStatus,
                'progress': student.matchingProgress,
                'started_at': student.matchingStartedAt,
                'completed_at': student.matchingCompletedAt,
                'error': student.matchingError
            }
        except StudentProfile.DoesNotExist:
            return {
                'status': 'not_found',
                'progress': 0,
                'started_at': None,
                'completed_at': None,
                'error': 'Student not found'
            }
