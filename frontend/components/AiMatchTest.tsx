'use client'

import React, { useState } from 'react'
import { useStudents, useGenerateMatches, useApiError } from '@/lib/hooks'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Loader2, Brain, Sparkles, Target, Users } from 'lucide-react'

export default function AiMatchTest() {
  const [selectedStudent, setSelectedStudent] = useState<string>('')
  const [matchType, setMatchType] = useState<'professor' | 'project'>('professor')
  const [useAI, setUseAI] = useState(true)
  const [matches, setMatches] = useState<any[]>([])
  const [isGenerating, setIsGenerating] = useState(false)
  
  // API hooks
  const { data: studentsData, isLoading: studentsLoading, error: studentsError } = useStudents()
  const generateMatchesMutation = useGenerateMatches()
  
  // Error handling
  const studentsErrorInfo = useApiError(studentsError)
  
  // Debug logging
  console.log('Students data:', studentsData)
  console.log('Students loading:', studentsLoading)
  console.log('Students error:', studentsError)
  
  const handleGenerateMatches = async () => {
    if (!selectedStudent) {
      alert('Please select a student first')
      return
    }
    
    setIsGenerating(true)
    try {
      const result = await generateMatchesMutation.mutateAsync({
        studentId: selectedStudent,
        matchType,
        useAI
      })
      
      if (result.success) {
        setMatches(result.data)
      } else {
        alert('Failed to generate matches')
      }
    } catch (error) {
      console.error('Error generating matches:', error)
      alert('Error generating matches')
    } finally {
      setIsGenerating(false)
    }
  }
  
  const getStudentName = (studentId: string) => {
    const student = studentsData?.data?.find(s => s.id === studentId)
    return student ? `${student.firstName} ${student.lastName}` : 'Unknown Student'
  }
  
  const renderMatchCard = (match: any, index: number) => (
    <Card key={match.id} className="mb-4">
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5 text-blue-600" />
              Match #{index + 1}
              {match.aiScore && (
                <Badge variant="secondary" className="ml-2">
                  <Brain className="h-3 w-3 mr-1" />
                  AI Score: {match.aiScore.toFixed(1)}
                </Badge>
              )}
            </CardTitle>
            <CardDescription>
              {match.matchType === 'professor' ? 'Professor Match' : 'Project Match'}
            </CardDescription>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-green-600">
              {match.score.toFixed(1)}
            </div>
            <div className="text-sm text-gray-500">Match Score</div>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {match.matchType === 'professor' && match.professor && (
          <div className="space-y-3">
            <div>
              <h4 className="font-semibold text-lg">{match.professor.name}</h4>
              <p className="text-gray-600">{match.professor.title} at {match.professor.institution}</p>
              <p className="text-sm text-gray-500">{match.professor.department}</p>
            </div>
            
            <div>
              <h5 className="font-medium mb-2">Research Areas:</h5>
              <div className="flex flex-wrap gap-1">
                {match.professor.researchAreas.map((area: string, idx: number) => (
                  <Badge key={idx} variant="outline" className="text-xs">
                    {area}
                  </Badge>
                ))}
              </div>
            </div>
          </div>
        )}
        
        {match.matchType === 'project' && match.project && (
          <div className="space-y-3">
            <div>
              <h4 className="font-semibold text-lg">{match.project.title}</h4>
              <p className="text-gray-600">{match.project.professor_name} - {match.project.professor_institution}</p>
            </div>
            
            <div>
              <p className="text-sm text-gray-700 mb-2">{match.project.summary}</p>
            </div>
            
            <div>
              <h5 className="font-medium mb-2">Research Areas:</h5>
              <div className="flex flex-wrap gap-1">
                {match.project.researchAreas.map((area: string, idx: number) => (
                  <Badge key={idx} variant="outline" className="text-xs">
                    {area}
                  </Badge>
                ))}
              </div>
            </div>
            
            <div className="flex gap-2 text-sm">
              <Badge variant="secondary">{match.project.compensation}</Badge>
              <Badge variant="outline">{match.project.location}</Badge>
              <Badge variant="outline">{match.project.hoursPerWeek}h/week</Badge>
            </div>
          </div>
        )}
        
        <div className="mt-4">
          <h5 className="font-medium mb-2">Highlights:</h5>
          <div className="flex flex-wrap gap-1">
            {match.highlights.map((highlight: string, idx: number) => (
              <Badge key={idx} variant="secondary" className="text-xs">
                {highlight}
              </Badge>
            ))}
          </div>
        </div>
        
        {match.aiExplanation && (
          <div className="mt-4 p-3 bg-blue-50 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Brain className="h-4 w-4 text-blue-600" />
              <h5 className="font-medium text-blue-800">AI Analysis</h5>
            </div>
            <p className="text-sm text-blue-700">{match.aiExplanation}</p>
          </div>
        )}
        
        {match.detailedScores && Object.keys(match.detailedScores).length > 0 && (
          <div className="mt-4">
            <h5 className="font-medium mb-2">Detailed Scores:</h5>
            <div className="space-y-2">
              {Object.entries(match.detailedScores).map(([key, value]) => (
                <div key={key} className="flex justify-between items-center">
                  <span className="text-sm capitalize">{key.replace(/_/g, ' ')}:</span>
                  <span className="text-sm font-medium">{value}/100</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  )
  
  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-6 w-6 text-purple-600" />
            AI-Enhanced Matching Test
          </CardTitle>
          <CardDescription>
            Test the Gemini AI-powered matching algorithm for students and professors/projects
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {/* Configuration Section */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="student">Select Student</Label>
                <Select value={selectedStudent} onValueChange={setSelectedStudent}>
                  <SelectTrigger>
                    <SelectValue placeholder="Choose a student" />
                  </SelectTrigger>
                  <SelectContent>
                    {studentsData?.data ? (
                      studentsData.data.map((student) => (
                        <SelectItem key={student.id} value={student.id}>
                          {student.firstName} {student.lastName} - {student.university}
                        </SelectItem>
                      ))
                    ) : (
                      <SelectItem value="" disabled>
                        No students available
                      </SelectItem>
                    )}
                  </SelectContent>
                </Select>
              </div>
              
              <div>
                <Label htmlFor="matchType">Match Type</Label>
                <Select value={matchType} onValueChange={(value: 'professor' | 'project') => setMatchType(value)}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="professor">
                      <div className="flex items-center gap-2">
                        <Users className="h-4 w-4" />
                        Professors
                      </div>
                    </SelectItem>
                    <SelectItem value="project">
                      <div className="flex items-center gap-2">
                        <Target className="h-4 w-4" />
                        Projects
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            
            {/* AI Toggle */}
            <div className="flex items-center space-x-2">
              <Switch
                id="use-ai"
                checked={useAI}
                onCheckedChange={setUseAI}
              />
              <Label htmlFor="use-ai" className="flex items-center gap-2">
                <Brain className="h-4 w-4" />
                Use AI-Enhanced Matching
              </Label>
            </div>
            
            {/* Generate Button */}
            <Button 
              onClick={handleGenerateMatches}
              disabled={!selectedStudent || isGenerating}
              className="w-full"
            >
              {isGenerating ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Generating AI Matches...
                </>
              ) : (
                <>
                  <Sparkles className="mr-2 h-4 w-4" />
                  Generate {useAI ? 'AI-Enhanced' : 'Basic'} Matches
                </>
              )}
            </Button>
            
            {/* Error Display */}
            {studentsError && (
              <Card className="border-red-200 bg-red-50">
                <CardContent className="pt-6">
                  <p className="text-red-600">Error: {studentsErrorInfo.message}</p>
                </CardContent>
              </Card>
            )}
            
            {/* Debug Information */}
            <Card className="border-blue-200 bg-blue-50">
              <CardContent className="pt-6">
                <h4 className="font-medium mb-2">Debug Info:</h4>
                <p className="text-sm">Loading: {studentsLoading ? 'Yes' : 'No'}</p>
                <p className="text-sm">Has Data: {studentsData ? 'Yes' : 'No'}</p>
                <p className="text-sm">Data Type: {typeof studentsData}</p>
                <p className="text-sm">Data Keys: {studentsData ? Object.keys(studentsData).join(', ') : 'None'}</p>
                <p className="text-sm">Students Count: {studentsData?.data?.length || 0}</p>
                <pre className="text-xs mt-2 bg-gray-100 p-2 rounded overflow-auto max-h-32">
                  {JSON.stringify(studentsData, null, 2)}
                </pre>
              </CardContent>
            </Card>
            
            {/* Results Section */}
            {matches.length > 0 && (
              <div className="mt-8">
                <h3 className="text-xl font-semibold mb-4">
                  Matches for {getStudentName(selectedStudent)}
                </h3>
                <div className="space-y-4">
                  {matches.map((match, index) => renderMatchCard(match, index))}
                </div>
              </div>
            )}
            
            {/* Loading State */}
            {studentsLoading && (
              <div className="text-center py-8">
                <Loader2 className="h-8 w-8 animate-spin mx-auto mb-2" />
                <p>Loading students...</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
