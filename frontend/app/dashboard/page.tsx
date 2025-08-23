'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Users, 
  MessageSquare, 
  MapPin, 
  BookOpen,
  Star,
  Loader2,
  ExternalLink
} from 'lucide-react'
import { matchApi } from '@/lib/api'
import { Match } from '@/types'

export default function DashboardPage() {
  const [matches, setMatches] = useState<Match[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        setLoading(true)
        setError(null)
        
        // For demo purposes, we'll use a hardcoded student ID
        // In a real app, this would come from authentication context
        const studentId = '1'
        
        // Fetch matches for the student
        const matchesResponse = await matchApi.getAll({ studentId })
        const matchesData = matchesResponse && typeof matchesResponse === 'object' && 'results' in matchesResponse 
          ? (matchesResponse as any).results 
          : (matchesResponse || [])
        
        // Deduplicate matches by professor ID - keep the highest scoring match for each professor
        const uniqueMatches = matchesData.reduce((acc: Match[], currentMatch: Match) => {
          const existingMatch = acc.find(match => match.professor.id === currentMatch.professor.id)
          
          if (!existingMatch) {
            acc.push(currentMatch)
          } else if (currentMatch.score > existingMatch.score) {
            // Replace with higher scoring match
            const index = acc.findIndex(match => match.professor.id === currentMatch.professor.id)
            acc[index] = currentMatch
          }
          
          return acc
        }, [])
        
        // Sort by score (highest first)
        uniqueMatches.sort((a: Match, b: Match) => b.score - a.score)
        
        setMatches(uniqueMatches)
        
      } catch (err) {
        console.error('Error fetching matches:', err)
        setError('Failed to load your matches')
      } finally {
        setLoading(false)
      }
    }

    fetchMatches()
  }, [])

  const getMatchStrengthColor = (score: number) => {
    if (score >= 90) return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    if (score >= 80) return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
    if (score >= 70) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
    return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
  }

  const getMatchStrengthLabel = (score: number) => {
    if (score >= 90) return 'Excellent Match'
    if (score >= 80) return 'Great Match'
    if (score >= 70) return 'Good Match'
    return 'Fair Match'
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin text-research-600 mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">Loading your matches...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-4">{error}</p>
          <Button onClick={() => window.location.reload()}>
            Try Again
          </Button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Your Research Matches
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Professors matched with your research interests and skills
          </p>
        </div>

        {/* Stats Summary */}
        <div className="mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <Users className="h-8 w-8 text-research-600" />
                  <div>
                    <p className="text-2xl font-bold">{matches.length}</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {matches.length === 1 ? 'Professor Match' : 'Professor Matches'}
                    </p>
                  </div>
                </div>
                {matches.length > 0 && (
                  <div className="text-right">
                    <p className="text-sm text-gray-600 dark:text-gray-400">Average Match Score</p>
                    <p className="text-2xl font-bold text-research-600">
                      {Math.round(matches.reduce((sum, match) => sum + match.score, 0) / matches.length)}%
                    </p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Matches List */}
        {matches.length === 0 ? (
          <Card>
            <CardContent className="pt-12 pb-12">
              <div className="text-center">
                <Users className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">No matches yet</h3>
                <p className="text-gray-600 dark:text-gray-400 mb-6 max-w-md mx-auto">
                  Complete your profile and search for research opportunities to find professor matches.
                </p>
                <div className="space-x-4">
                  <Button>
                    <BookOpen className="h-4 w-4 mr-2" />
                    Complete Profile
                  </Button>
                  <Button variant="outline">
                    <ExternalLink className="h-4 w-4 mr-2" />
                    Search Opportunities
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {matches.map((match) => (
              <Card key={match.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <CardTitle className="text-xl">
                          {match.professor.name}
                        </CardTitle>
                        <Badge className={`${getMatchStrengthColor(match.score)}`}>
                          {getMatchStrengthLabel(match.score)}
                        </Badge>
                      </div>
                      <CardDescription className="text-base">
                        {match.professor.title} • {match.professor.department}
                      </CardDescription>
                      <div className="flex items-center space-x-4 mt-2 text-sm text-gray-600 dark:text-gray-400">
                        <div className="flex items-center space-x-1">
                          <MapPin className="h-4 w-4" />
                          <span>{match.professor.institution}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Star className="h-4 w-4" />
                          <span>{match.score}% Match</span>
                        </div>
                        {match.aiScore && (
                          <div className="flex items-center space-x-1">
                            <BookOpen className="h-4 w-4" />
                            <span>AI Enhanced: {match.aiScore}%</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent>
                  <div className="space-y-4">
                    {/* Research Areas */}
                    <div>
                      <h4 className="font-medium mb-2 text-sm text-gray-700 dark:text-gray-300">
                        Research Areas
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {match.professor.researchAreas.slice(0, 5).map((area, index) => (
                          <Badge key={index} variant="secondary" className="text-xs">
                            {area}
                          </Badge>
                        ))}
                        {match.professor.researchAreas.length > 5 && (
                          <Badge variant="outline" className="text-xs">
                            +{match.professor.researchAreas.length - 5} more
                          </Badge>
                        )}
                      </div>
                    </div>

                    {/* Match Highlights */}
                    {match.highlights && match.highlights.length > 0 && (
                      <div>
                        <h4 className="font-medium mb-2 text-sm text-gray-700 dark:text-gray-300">
                          Why This Match Works
                        </h4>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          {match.highlights.slice(0, 2).join(' • ')}
                        </div>
                      </div>
                    )}

                    {/* AI Explanation */}
                    {match.aiExplanation && (
                      <div>
                        <h4 className="font-medium mb-2 text-sm text-gray-700 dark:text-gray-300">
                          AI Analysis
                        </h4>
                        <div className="text-sm text-gray-600 dark:text-gray-400">
                          {match.aiExplanation.length > 150 
                            ? `${match.aiExplanation.substring(0, 150)}...` 
                            : match.aiExplanation
                          }
                        </div>
                      </div>
                    )}

                    {/* Action Buttons */}
                    <div className="flex items-center justify-between pt-4 border-t">
                      <div className="text-xs text-gray-500">
                        Matched on {new Date(match.createdAt).toLocaleDateString()}
                      </div>
                      
                      <div className="flex space-x-2">
                        <Button variant="outline" size="sm">
                          <MessageSquare className="h-4 w-4 mr-2" />
                          Contact
                        </Button>
                        <Button size="sm">
                          <BookOpen className="h-4 w-4 mr-2" />
                          View Profile
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
