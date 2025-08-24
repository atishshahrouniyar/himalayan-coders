'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  User, 
  BookOpen, 
  Target, 
  Calendar, 
  FileText, 
  CheckCircle,
  ArrowRight,
  ArrowLeft,
  Loader2
} from 'lucide-react'
import { OnboardingStep, OnboardingProgress } from '@/types'
import { studentApi, professorApi } from '@/lib/api'
import { userSession } from '@/lib/utils'

const ONBOARDING_STEPS: OnboardingStep[] = [
  {
    id: 'role',
    title: 'Choose Your Role',
    description: 'Are you a student looking for research opportunities or a professor seeking students?',
    isCompleted: false,
    isRequired: true
  },
  {
    id: 'basics',
    title: 'Basic Information',
    description: 'Tell us about yourself and your academic background',
    isCompleted: false,
    isRequired: true
  },
  {
    id: 'interests',
    title: 'Research Interests',
    description: 'What areas of research are you interested in?',
    isCompleted: false,
    isRequired: true
  },
  {
    id: 'skills',
    title: 'Skills & Experience',
    description: 'What skills and experience do you bring? This helps us find better matches.',
    isCompleted: false,
    isRequired: true
  },
  {
    id: 'availability',
    title: 'Availability & Preferences',
    description: 'When are you available and what are your preferences?',
    isCompleted: false,
    isRequired: true
  },
  {
    id: 'documents',
    title: 'Documents & Links',
    description: 'Upload your CV and add relevant links',
    isCompleted: false,
    isRequired: false
  },
  {
    id: 'review',
    title: 'Review & Complete',
    description: 'Review your profile and complete the setup',
    isCompleted: false,
    isRequired: true
  }
]

export default function OnboardingPage() {
  const router = useRouter()
  const [currentStep, setCurrentStep] = useState(0)
  const [userRole, setUserRole] = useState<'student' | 'professor' | null>(null)
  const [profileData, setProfileData] = useState<any>({})
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const progress: OnboardingProgress = {
    currentStep: currentStep + 1,
    totalSteps: ONBOARDING_STEPS.length,
    completedSteps: ONBOARDING_STEPS.filter(step => step.isCompleted).length,
    progress: Math.round(((currentStep + 1) / ONBOARDING_STEPS.length) * 100)
  }

  const handleNext = () => {
    if (currentStep < ONBOARDING_STEPS.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  const handleComplete = async () => {
    if (!userRole) {
      setError('Please select a role')
      return
    }

    // Validate required fields
    const requiredFields = ['firstName', 'lastName', 'email', 'university']
    const missingFields = requiredFields.filter(field => !profileData[field])
    
    if (missingFields.length > 0) {
      setError(`Please fill in all required fields: ${missingFields.join(', ')}`)
      return
    }

    setIsSubmitting(true)
    setError(null)

    try {
      // Prepare the profile data
      const profilePayload = {
        firstName: profileData.firstName,
        lastName: profileData.lastName,
        email: profileData.email,
        university: profileData.university,
        primaryInterests: profileData.interests || [],
        programmingSkills: profileData.programmingSkills || [],
        startDate: profileData.startDate,
        githubUrl: profileData.githubUrl,
        // Add default values for required fields
        department: profileData.department || 'Computer Science',
        degreeLevel: profileData.degreeLevel || 'BS',
        gpa: profileData.gpa || 3.5,
        availability: profileData.availability || 'Full-time',
        researchExperience: profileData.researchExperience || 'None',
        // Optional fields - no default values needed
        year: profileData.year,
        semester: profileData.semester,
        hoursPerWeek: profileData.hoursPerWeek,
        publications: profileData.publications || [],
        awards: profileData.awards || [],
        languages: profileData.languages || ['English'],
        linkedinUrl: profileData.linkedinUrl || '',
        personalWebsite: profileData.personalWebsite || '',
        bio: profileData.bio || '',
        acceptingStudents: userRole === 'professor' ? true : undefined,
        researchAreas: userRole === 'professor' ? (profileData.interests || []) : undefined,
        currentPosition: userRole === 'professor' ? 'Professor' : undefined,
        yearsOfExperience: userRole === 'professor' ? 5 : undefined,
        labWebsite: userRole === 'professor' ? profileData.personalWebsite || '' : undefined,
        fundingAvailable: userRole === 'professor' ? true : undefined,
        mentorshipStyle: userRole === 'professor' ? 'Collaborative' : undefined,
        grants: userRole === 'professor' ? (profileData.grants || []) : undefined,
        collaborations: userRole === 'professor' ? (profileData.collaborations || []) : undefined,
        teachingExperience: userRole === 'professor' ? (profileData.teachingExperience || []) : undefined,
        industryConnections: userRole === 'professor' ? (profileData.industryConnections || []) : undefined,
        internationalExperience: userRole === 'professor' ? (profileData.internationalExperience || []) : undefined,
        patents: userRole === 'professor' ? (profileData.patents || []) : undefined,
        honors: userRole === 'professor' ? (profileData.honors || []) : undefined,
        service: userRole === 'professor' ? (profileData.service || []) : undefined,
        outreach: userRole === 'professor' ? (profileData.outreach || []) : undefined,
        diversity: userRole === 'professor' ? (profileData.diversity || []) : undefined,
        innovation: userRole === 'professor' ? (profileData.innovation || []) : undefined,
        leadership: userRole === 'professor' ? (profileData.leadership || []) : undefined,
        mentorship: userRole === 'professor' ? (profileData.mentorship || []) : undefined,
        research: userRole === 'professor' ? (profileData.research || []) : undefined,
        education: userRole === 'professor' ? (profileData.education || []) : undefined,
        work: userRole === 'professor' ? (profileData.work || []) : undefined,
        skills: userRole === 'professor' ? (profileData.skills || []) : undefined,
        projects: userRole === 'professor' ? (profileData.projects || []) : undefined,
      }

      // Submit to appropriate API based on user role
      let createdProfile
      if (userRole === 'student') {
        createdProfile = await studentApi.create(profilePayload)
        // Save user session data
        userSession.saveUserSession(createdProfile.id, 'student')
        
        // Show success message for students
        setError(null)
        alert('Profile created successfully! We are now finding the best professors for your research interests. This may take a few minutes.')
      } else {
        createdProfile = await professorApi.create(profilePayload)
        // Save user session data
        userSession.saveUserSession(createdProfile.id, 'professor')
      }

      // Redirect to dashboard on success
      router.push('/dashboard')
    } catch (err: any) {
      console.error('Error creating profile:', err)
      setError(err.message || 'Failed to create profile. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const renderStepContent = () => {
    const step = ONBOARDING_STEPS[currentStep]
    
    switch (step.id) {
      case 'role':
        return (
          <div className="space-y-6">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-bold mb-2">Welcome to ResearchMatch!</h2>
              <p className="text-gray-600 dark:text-gray-400">
                Let's get started by understanding your role in the research community.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <Card 
                className={`cursor-pointer transition-all hover:shadow-lg ${
                  userRole === 'student' ? 'ring-2 ring-research-500 bg-research-50 dark:bg-research-950' : ''
                }`}
                onClick={() => setUserRole('student')}
              >
                <CardHeader className="text-center">
                  <div className="mx-auto w-16 h-16 bg-research-100 dark:bg-research-900 rounded-full flex items-center justify-center mb-4">
                    <BookOpen className="h-8 w-8 text-research-600" />
                  </div>
                  <CardTitle>Student</CardTitle>
                  <CardDescription>
                    I'm a student looking for research opportunities and mentorship
                  </CardDescription>
                </CardHeader>
              </Card>

              <Card 
                className={`cursor-pointer transition-all hover:shadow-lg ${
                  userRole === 'professor' ? 'ring-2 ring-research-500 bg-research-50 dark:bg-research-950' : ''
                }`}
                onClick={() => setUserRole('professor')}
              >
                <CardHeader className="text-center">
                  <div className="mx-auto w-16 h-16 bg-research-100 dark:bg-research-900 rounded-full flex items-center justify-center mb-4">
                    <User className="h-8 w-8 text-research-600" />
                  </div>
                  <CardTitle>Professor/Researcher</CardTitle>
                  <CardDescription>
                    I'm a professor or researcher looking for students to join my research
                  </CardDescription>
                </CardHeader>
              </Card>
            </div>
          </div>
        )

      case 'basics':
        return (
          <div className="space-y-6">
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium mb-2">First Name</label>
                <input 
                  type="text" 
                  className="input-field"
                  placeholder="Enter your first name"
                  value={profileData.firstName || ''}
                  onChange={(e) => setProfileData({...profileData, firstName: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Last Name</label>
                <input 
                  type="text" 
                  className="input-field"
                  placeholder="Enter your last name"
                  value={profileData.lastName || ''}
                  onChange={(e) => setProfileData({...profileData, lastName: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Email</label>
                <input 
                  type="email" 
                  className="input-field"
                  placeholder="Enter your email"
                  value={profileData.email || ''}
                  onChange={(e) => setProfileData({...profileData, email: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Undergrad University</label>
                <input 
                  type="text" 
                  className="input-field"
                  placeholder="Enter your undergraduate university"
                  value={profileData.university || ''}
                  onChange={(e) => setProfileData({...profileData, university: e.target.value})}
                />
              </div>
            </div>
          </div>
        )

      case 'interests':
        return (
          <div className="space-y-6">
            
            <div>
              <label className="block text-sm font-medium mb-4">Primary Research Areas</label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {['NLP', 'Computer Vision', 'HCI', 'Robotics', 'Bioinformatics', 'Machine Learning', 'Data Science', 'Cybersecurity', 'Quantum Computing', 'Materials Science'].map((area) => (
                  <label key={area} className="flex items-center space-x-2 cursor-pointer">
                    <input 
                      type="checkbox" 
                      className="rounded border-gray-300 text-research-600 focus:ring-research-500"
                      checked={profileData.interests?.includes(area) || false}
                      onChange={(e) => {
                        const currentInterests = profileData.interests || []
                        if (e.target.checked) {
                          setProfileData({...profileData, interests: [...currentInterests, area]})
                        } else {
                          setProfileData({...profileData, interests: currentInterests.filter((i: string) => i !== area)})
                        }
                      }}
                    />
                    <span className="text-sm">{area}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        )

      case 'skills':
        return (
          <div className="space-y-6">
            
            <div>
              <label className="block text-sm font-medium mb-4">Programming Languages</label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {['Python', 'R', 'MATLAB', 'C++', 'Java', 'JavaScript'].map((skill) => (
                  <label key={skill} className="flex items-center space-x-2 cursor-pointer">
                    <input 
                      type="checkbox" 
                      className="rounded border-gray-300 text-research-600 focus:ring-research-500"
                      checked={profileData.programmingSkills?.includes(skill) || false}
                      onChange={(e) => {
                        const currentSkills = profileData.programmingSkills || []
                        if (e.target.checked) {
                          setProfileData({...profileData, programmingSkills: [...currentSkills, skill]})
                        } else {
                          setProfileData({...profileData, programmingSkills: currentSkills.filter((s: string) => s !== skill)})
                        }
                      }}
                    />
                    <span className="text-sm">{skill}</span>
                  </label>
                ))}
              </div>
            </div>
          </div>
        )

      case 'availability':
        return (
          <div className="space-y-6">
            
            <div className="max-w-md mx-auto">
              <div>
                <label className="block text-sm font-medium mb-2">Your Approximate Graduate Start Preference</label>
                <input 
                  type="date" 
                  className="input-field"
                  value={profileData.startDate || ''}
                  onChange={(e) => setProfileData({...profileData, startDate: e.target.value})}
                />
              </div>
            </div>
          </div>
        )

      case 'documents':
        return (
          <div className="space-y-6">
            
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium mb-2">CV/Resume</label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <FileText className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                  <p className="text-sm text-gray-600">Drop your CV here or click to browse</p>
                  <p className="text-xs text-gray-500 mt-2">PDF, max 5MB</p>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">GitHub Profile</label>
                <input 
                  type="url" 
                  className="input-field"
                  placeholder="https://github.com/username"
                  value={profileData.githubUrl || ''}
                  onChange={(e) => setProfileData({...profileData, githubUrl: e.target.value})}
                />
              </div>
            </div>
          </div>
        )

      case 'review':
        return (
          <div className="space-y-6">
            
            <Card>
              <CardHeader>
                <CardTitle>Profile Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <span className="text-sm font-medium text-gray-500">Name:</span>
                    <p>{profileData.firstName} {profileData.lastName}</p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">Role:</span>
                    <p className="capitalize">{userRole}</p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">University:</span>
                    <p>{profileData.university}</p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">Interests:</span>
                    <div className="flex flex-wrap gap-1 mt-1">
                      {profileData.interests?.map((interest: string) => (
                        <Badge key={interest} variant="secondary">{interest}</Badge>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <div className="container mx-auto px-4 max-w-4xl">
        {/* Progress Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-2xl font-bold">Complete Your Profile</h1>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              Step {progress.currentStep} of {progress.totalSteps}
            </div>
          </div>
          <Progress value={progress.progress} className="h-2" />
        </div>

        {/* Step Content */}
        <Card className="mb-8">
          <CardHeader>
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-research-100 dark:bg-research-900 rounded-full flex items-center justify-center">
                {ONBOARDING_STEPS[currentStep].isCompleted ? (
                  <CheckCircle className="h-5 w-5 text-research-600" />
                ) : (
                  <span className="text-sm font-semibold text-research-600">
                    {currentStep + 1}
                  </span>
                )}
              </div>
              <div>
                <CardTitle>{ONBOARDING_STEPS[currentStep].title}</CardTitle>
                <CardDescription>{ONBOARDING_STEPS[currentStep].description}</CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            {renderStepContent()}
          </CardContent>
        </Card>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between">
          <Button
            variant="outline"
            onClick={handlePrevious}
            disabled={currentStep === 0 || isSubmitting}
            className="flex items-center space-x-2"
          >
            <ArrowLeft className="h-4 w-4" />
            Previous
          </Button>

          {currentStep === ONBOARDING_STEPS.length - 1 ? (
            <Button
              onClick={handleComplete}
              disabled={isSubmitting}
              className="bg-research-600 hover:bg-research-700 flex items-center space-x-2"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Creating Profile...
                </>
              ) : (
                <>
                  Complete Setup
                  <CheckCircle className="h-4 w-4" />
                </>
              )}
            </Button>
          ) : (
            <Button
              onClick={handleNext}
              disabled={(!userRole && currentStep === 0) || isSubmitting}
              className="bg-research-600 hover:bg-research-700 flex items-center space-x-2"
            >
              Next
              <ArrowRight className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
