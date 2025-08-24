import google.generativeai as genai
from django.conf import settings
from typing import List, Dict, Any, Tuple
import json

class GeminiMatchingService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def analyze_student_profile(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a student profile using Gemini AI to extract key insights
        """
        prompt = f"""
        Analyze this student profile and provide insights for matching:
        
        Student Profile:
        - Name: {student_data.get('firstName', '')} {student_data.get('lastName', '')}
        - University: {student_data.get('university', '')}
        - Department: {student_data.get('department', '')}
        - Degree Level: {student_data.get('degreeLevel', '')}
        - Primary Interests: {', '.join(student_data.get('primaryInterests', []))}
        - Methods: {', '.join(student_data.get('methods', []))}
        - Programming Skills: {json.dumps(student_data.get('programmingSkills', []))}
        - Lab Skills: {', '.join(student_data.get('labSkills', []))}
        - Statistical Skills: {', '.join(student_data.get('statisticalSkills', []))}
        - Hours per Week: {student_data.get('hoursPerWeek', 0)}
        - Compensation Preference: {student_data.get('compensation', '')}
        - Location Preference: {student_data.get('remotePreference', '')}
        
        Please provide:
        1. Key strengths and expertise areas
        2. Research interests summary
        3. Technical skills assessment
        4. Ideal professor characteristics
        5. Matching priorities
        
        Return as JSON with keys: strengths, interests_summary, technical_skills, ideal_professor, priorities
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Error analyzing student profile: {e}")
            return {
                "strengths": student_data.get('primaryInterests', []),
                "interests_summary": "Research interests analysis unavailable",
                "technical_skills": student_data.get('programmingSkills', []),
                "ideal_professor": "Professor preferences analysis unavailable",
                "priorities": ["research_alignment", "skill_match"]
            }
    
    def analyze_professor_profile(self, professor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a professor profile using Gemini AI to extract key insights
        """
        prompt = f"""
        Analyze this professor profile and provide insights for matching:
        
        Professor Profile:
        - Name: {professor_data.get('name', '')}
        - Title: {professor_data.get('title', '')}
        - Institution: {professor_data.get('institution', '')}
        - Department: {professor_data.get('department', '')}
        - Research Areas: {', '.join(professor_data.get('researchAreas', []))}
        - Research Description: {professor_data.get('researchDescription', '')}
        - Methods: {', '.join(professor_data.get('methods', []))}
        - Accepting Students: {professor_data.get('acceptingStudents', False)}
        - Preferred Degree Levels: {', '.join(professor_data.get('preferredDegreeLevels', []))}
        - Prerequisites: {professor_data.get('prerequisites', '')}
        
        Please provide:
        1. Research focus and expertise areas
        2. Ideal student characteristics
        3. Research requirements and expectations
        4. Mentoring style indicators
        5. Collaboration preferences
        
        Return as JSON with keys: research_focus, ideal_student, research_requirements, mentoring_style, collaboration_preferences
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Error analyzing professor profile: {e}")
            return {
                "research_focus": professor_data.get('researchAreas', []),
                "ideal_student": "Student preferences analysis unavailable",
                "research_requirements": professor_data.get('prerequisites', ''),
                "mentoring_style": "Mentoring style analysis unavailable",
                "collaboration_preferences": ["research_alignment", "skill_match"]
            }
    

    
    def calculate_ai_match_score(self, student_data: Dict[str, Any], professor_data: Dict[str, Any]) -> Tuple[float, List[str], Dict[str, Any]]:
        """
        Calculate an AI-enhanced match score between student and professor
        """
        # Analyze student profile
        student_analysis = self.analyze_student_profile(student_data)
        
        # Student-Professor matching
        professor_analysis = self.analyze_professor_profile(professor_data)
        
        prompt = f"""
        Calculate a match score between this student and professor:
        
        Student Analysis:
        {json.dumps(student_analysis, indent=2)}
        
        Professor Analysis:
        {json.dumps(professor_analysis, indent=2)}
        
        Consider:
        1. Research area alignment (0-100)
        2. Skill compatibility (0-100)
        3. Academic level fit (0-100)
        4. Availability and commitment match (0-100)
        5. Learning and growth potential (0-100)
        
        Return as JSON with:
        - overall_score: weighted average (0-100)
        - highlights: list of key matching points
        - detailed_scores: object with individual scores
        - reasoning: explanation of the match
        """
        
        try:
            response = self.model.generate_content(prompt)
            match_result = json.loads(response.text)
            
            return (
                match_result.get('overall_score', 0),
                match_result.get('highlights', []),
                match_result
            )
        except Exception as e:
            print(f"Error calculating AI match score: {e}")
            # Fallback to basic matching
            return self._calculate_basic_match_score(student_data, professor_data)
    
    def _calculate_basic_match_score(self, student_data: Dict[str, Any], professor_data: Dict[str, Any]) -> Tuple[float, List[str], Dict[str, Any]]:
        """
        Fallback basic matching algorithm when AI analysis fails
        """
        # Basic student-professor matching
        student_interests = set(student_data.get('primaryInterests', []))
        professor_areas = set(professor_data.get('researchAreas', []))
        
        common_interests = student_interests & professor_areas
        score = len(common_interests) / max(len(student_interests), 1) * 100
        
        return (
            score,
            list(common_interests),
            {"overall_score": score, "highlights": list(common_interests)}
        )
    
    def generate_match_explanation(self, student_data: Dict[str, Any], professor_data: Dict[str, Any], match_score: float = 0) -> str:
        """
        Generate a human-readable explanation of the match
        """
        prompt = f"""
        Generate a brief, friendly explanation of why this student and professor are a good match:
        
        Student: {student_data.get('firstName', '')} {student_data.get('lastName', '')} ({student_data.get('university', '')})
        Interests: {', '.join(student_data.get('primaryInterests', []))}
        
        Professor: {professor_data.get('name', '')} ({professor_data.get('institution', '')})
        Research Areas: {', '.join(professor_data.get('researchAreas', []))}
        
        Match Score: {match_score}/100
        
        Write 2-3 sentences explaining the match in a positive, encouraging tone.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating match explanation: {e}")
            return f"This match has a score of {round(match_score, 2)}/100 based on research area alignment and skill compatibility."

    def analyze_match(self, student_data: Dict[str, Any], professor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a match between a student and professor using Gemini AI
        """
        try:
            score, highlights, detailed_analysis = self.calculate_ai_match_score(student_data, professor_data)
            explanation = self.generate_match_explanation(student_data, professor_data, score)
            
            return {
                'score': round(score, 2),
                'explanation': explanation,
                'highlights': highlights,
                'analysis': detailed_analysis
            }
        except Exception as e:
            print(f"Error in analyze_match: {e}")
            # Fallback to basic matching
            score, highlights, _ = self._calculate_basic_match_score(student_data, professor_data)
            return {
                'score': round(score, 2),
                'explanation': f"This match has a score of {round(score, 2)}/100 based on research area alignment and skill compatibility.",
                'highlights': highlights,
                'analysis': {'overall_score': round(score, 2), 'highlights': highlights}
            }
