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
        4. Ideal project characteristics
        5. Matching priorities
        
        Return as JSON with keys: strengths, interests_summary, technical_skills, ideal_project, priorities
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
                "ideal_project": "Project preferences analysis unavailable",
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
        3. Project requirements and expectations
        4. Mentoring style indicators
        5. Collaboration preferences
        
        Return as JSON with keys: research_focus, ideal_student, project_requirements, mentoring_style, collaboration_preferences
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Error analyzing professor profile: {e}")
            return {
                "research_focus": professor_data.get('researchAreas', []),
                "ideal_student": "Student preferences analysis unavailable",
                "project_requirements": professor_data.get('prerequisites', ''),
                "mentoring_style": "Mentoring style analysis unavailable",
                "collaboration_preferences": ["research_alignment", "skill_match"]
            }
    
    def analyze_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a research project using Gemini AI to extract key insights
        """
        prompt = f"""
        Analyze this research project and provide insights for matching:
        
        Project Details:
        - Title: {project_data.get('title', '')}
        - Summary: {project_data.get('summary', '')}
        - Description: {project_data.get('description', '')}
        - Research Areas: {', '.join(project_data.get('researchAreas', []))}
        - Techniques: {', '.join(project_data.get('techniques', []))}
        - Desired Skills: {json.dumps(project_data.get('desiredSkills', []))}
        - Hours per Week: {project_data.get('hoursPerWeek', 0)}
        - Compensation: {project_data.get('compensation', '')}
        - Location: {project_data.get('location', '')}
        
        Please provide:
        1. Project complexity and scope
        2. Required skills and experience level
        3. Learning opportunities
        4. Ideal candidate characteristics
        5. Project benefits for students
        
        Return as JSON with keys: complexity, required_skills, learning_opportunities, ideal_candidate, benefits
        """
        
        try:
            response = self.model.generate_content(prompt)
            return json.loads(response.text)
        except Exception as e:
            print(f"Error analyzing project: {e}")
            return {
                "complexity": "Project complexity analysis unavailable",
                "required_skills": project_data.get('desiredSkills', []),
                "learning_opportunities": "Learning opportunities analysis unavailable",
                "ideal_candidate": "Ideal candidate analysis unavailable",
                "benefits": ["research_experience", "skill_development"]
            }
    
    def calculate_ai_match_score(self, student_data: Dict[str, Any], professor_data: Dict[str, Any] = None, project_data: Dict[str, Any] = None) -> Tuple[float, List[str], Dict[str, Any]]:
        """
        Calculate an AI-enhanced match score between student and professor/project
        """
        # Analyze student profile
        student_analysis = self.analyze_student_profile(student_data)
        
        if professor_data:
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
            
        elif project_data:
            # Student-Project matching
            project_analysis = self.analyze_project(project_data)
            
            prompt = f"""
            Calculate a match score between this student and research project:
            
            Student Analysis:
            {json.dumps(student_analysis, indent=2)}
            
            Project Analysis:
            {json.dumps(project_analysis, indent=2)}
            
            Consider:
            1. Research area alignment (0-100)
            2. Skill requirements match (0-100)
            3. Time commitment compatibility (0-100)
            4. Learning opportunity fit (0-100)
            5. Career development potential (0-100)
            
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
            return self._calculate_basic_match_score(student_data, professor_data, project_data)
    
    def _calculate_basic_match_score(self, student_data: Dict[str, Any], professor_data: Dict[str, Any] = None, project_data: Dict[str, Any] = None) -> Tuple[float, List[str], Dict[str, Any]]:
        """
        Fallback basic matching algorithm when AI analysis fails
        """
        if professor_data:
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
        
        elif project_data:
            # Basic student-project matching
            student_interests = set(student_data.get('primaryInterests', []))
            project_areas = set(project_data.get('researchAreas', []))
            
            common_interests = student_interests & project_areas
            score = len(common_interests) / max(len(student_interests), 1) * 100
            
            return (
                score,
                list(common_interests),
                {"overall_score": score, "highlights": list(common_interests)}
            )
        
        return (0, [], {})
    
    def generate_match_explanation(self, student_data: Dict[str, Any], professor_data: Dict[str, Any] = None, project_data: Dict[str, Any] = None, match_score: float = 0) -> str:
        """
        Generate a human-readable explanation of the match
        """
        if professor_data:
            prompt = f"""
            Generate a brief, friendly explanation of why this student and professor are a good match:
            
            Student: {student_data.get('firstName', '')} {student_data.get('lastName', '')} ({student_data.get('university', '')})
            Interests: {', '.join(student_data.get('primaryInterests', []))}
            
            Professor: {professor_data.get('name', '')} ({professor_data.get('institution', '')})
            Research Areas: {', '.join(professor_data.get('researchAreas', []))}
            
            Match Score: {match_score}/100
            
            Write 2-3 sentences explaining the match in a positive, encouraging tone.
            """
        elif project_data:
            prompt = f"""
            Generate a brief, friendly explanation of why this student and project are a good match:
            
            Student: {student_data.get('firstName', '')} {student_data.get('lastName', '')} ({student_data.get('university', '')})
            Interests: {', '.join(student_data.get('primaryInterests', []))}
            
            Project: {project_data.get('title', '')}
            Research Areas: {', '.join(project_data.get('researchAreas', []))}
            
            Match Score: {match_score}/100
            
            Write 2-3 sentences explaining the match in a positive, encouraging tone.
            """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating match explanation: {e}")
            return f"This match has a score of {match_score}/100 based on research area alignment and skill compatibility."
