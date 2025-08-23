'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { 
  Search as SearchIcon, 
  Filter, 
  MapPin, 
  Clock, 
  Users, 
  BookOpen,
  Star,
  MessageSquare,
  ExternalLink,
  Loader2
} from 'lucide-react'
import { RESEARCH_AREAS, METHODS_TECHNIQUES, DEGREE_LEVELS, COMPENSATION_TYPES } from '@/lib/constants'
import { professorApi, searchApi } from '@/lib/api'
import { ProfessorProfile } from '@/types'

export default function SearchPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedAreas, setSelectedAreas] = useState<string[]>([])
  const [selectedMethods, setSelectedMethods] = useState<string[]>([])
  const [selectedLevels, setSelectedLevels] = useState<string[]>([])
  const [selectedCompensation, setSelectedCompensation] = useState<string[]>([])
  const [professors, setProfessors] = useState<ProfessorProfile[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        const response = await professorApi.getAll({
          query: searchQuery,
          tags: selectedAreas,
          department: selectedAreas.length > 0 ? selectedAreas[0] : undefined
        })
        // Handle paginated response
        let professorsData: ProfessorProfile[] = []
        if (response && typeof response === 'object' && 'results' in response && Array.isArray((response as any).results)) {
          professorsData = (response as any).results
        } else if (Array.isArray(response)) {
          professorsData = response
        }
        
        setProfessors(professorsData)
      } catch (err) {
        console.error('Error fetching data:', err)
        setError('Failed to load data')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [searchQuery, selectedAreas, selectedMethods, selectedLevels, selectedCompensation])

  const handleSearch = async () => {
    if (!searchQuery.trim()) return

    try {
      setLoading(true)
      setError(null)

      const response = await searchApi.global(searchQuery, 'professors')
      setProfessors(response.professors || [])
    } catch (err) {
      console.error('Error searching:', err)
      setError('Search failed')
    } finally {
      setLoading(false)
    }
  }

  const filteredProfessors = (Array.isArray(professors) ? professors : []).filter(prof => {
    if (searchQuery && !prof.name.toLowerCase().includes(searchQuery.toLowerCase()) && 
        !(prof.researchAreas || []).some(area => area.toLowerCase().includes(searchQuery.toLowerCase()))) {
      return false
    }
    if (selectedAreas.length > 0 && !selectedAreas.some(area => (prof.researchAreas || []).includes(area))) {
      return false
    }
    if (selectedMethods.length > 0 && !selectedMethods.some(method => (prof.methods || []).includes(method))) {
      return false
    }
    if (selectedLevels.length > 0 && !selectedLevels.some(level => 
      (prof.preferredDegreeLevels || []).includes(level as 'BS' | 'MS' | 'PhD'))) {
      return false
    }
    return true
  })

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

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Search Research Opportunities
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Find professors that match your interests and skills
          </p>
        </div>

        {/* Search Bar and Filters */}
        <div className="mb-8">
          <div className="flex flex-col lg:flex-row gap-4 mb-4">
            <div className="flex-1 relative">
              <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder="Search professors..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button
              variant="outline"
              onClick={handleSearch}
              className="flex items-center space-x-2"
            >
              <SearchIcon className="h-4 w-4" />
              Search
            </Button>
            <Button
              variant="outline"
              onClick={() => setSelectedAreas([])}
              className="flex items-center space-x-2"
            >
              <Filter className="h-4 w-4" />
              Clear Filters
            </Button>
          </div>

          {/* Filters Panel */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="text-lg">Filters</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {/* Research Areas */}
                <div>
                  <label className="block text-sm font-medium mb-3">Research Areas</label>
                  <div className="space-y-2 max-h-32 overflow-y-auto">
                    {RESEARCH_AREAS.slice(0, 10).map((area) => (
                      <label key={area} className="flex items-center space-x-2 cursor-pointer">
                        <input
                          type="checkbox"
                          className="rounded border-gray-300 text-research-600 focus:ring-research-500"
                          checked={selectedAreas.includes(area)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setSelectedAreas([...selectedAreas, area])
                            } else {
                              setSelectedAreas(selectedAreas.filter(a => a !== area))
                            }
                          }}
                        />
                        <span className="text-sm">{area}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Methods */}
                <div>
                  <label className="block text-sm font-medium mb-3">Methods</label>
                  <div className="space-y-2 max-h-32 overflow-y-auto">
                    {METHODS_TECHNIQUES.slice(0, 10).map((method) => (
                      <label key={method} className="flex items-center space-x-2 cursor-pointer">
                        <input
                          type="checkbox"
                          className="rounded border-gray-300 text-research-600 focus:ring-research-500"
                          checked={selectedMethods.includes(method)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setSelectedMethods([...selectedMethods, method])
                            } else {
                              setSelectedMethods(selectedMethods.filter(m => m !== method))
                            }
                          }}
                        />
                        <span className="text-sm">{method}</span>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Degree Level */}
                <div>
                  <label className="block text-sm font-medium mb-3">Degree Level</label>
                  <select
                    className="input-field"
                    value={selectedLevels}
                    onChange={(e) => {
                      const selected = Array.from(e.target.selectedOptions, option => option.value)
                      setSelectedLevels(selected)
                    }}
                    multiple
                  >
                    {DEGREE_LEVELS.map((level) => (
                      <option key={level} value={level}>{level}</option>
                    ))}
                  </select>
                </div>

                {/* Compensation */}
                <div>
                  <label className="block text-sm font-medium mb-3">Compensation</label>
                  <select
                    className="input-field"
                    value={selectedCompensation}
                    onChange={(e) => {
                      const selected = Array.from(e.target.selectedOptions, option => option.value)
                      setSelectedCompensation(selected)
                    }}
                    multiple
                  >
                    {COMPENSATION_TYPES.map((type) => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Results */}
        <div className="space-y-6">
          {loading && (
            <div className="flex justify-center items-center py-12">
              <Loader2 className="h-12 w-12 text-research-600 animate-spin" />
            </div>
          )}
          {error && (
            <div className="text-center text-red-500 py-12">{error}</div>
          )}
          {!loading && !error && (
            <>
              <h2 className="text-xl font-semibold">
                {filteredProfessors.length} Professors
              </h2>
              {filteredProfessors.map((professor) => (
                <Card key={professor.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-xl">{professor.name}</CardTitle>
                        <CardDescription>
                          {professor.title} • {professor.department} • {professor.institution}
                        </CardDescription>
                      </div>
                      <div className="text-right">
                        <Badge variant="secondary">
                          {professor.acceptingStudents ? 'Accepting Students' : 'Not Accepting'}
                        </Badge>
                        <div className="text-2xl font-bold text-research-600 mt-1">
                          {professor.profileCompleteness}%
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <h4 className="font-medium mb-2">Research Areas</h4>
                        <div className="flex flex-wrap gap-2">
                          {(professor.researchAreas || []).map((area) => (
                            <Badge key={area} variant="secondary">{area}</Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div>
                        <h4 className="font-medium mb-2">Methods & Techniques</h4>
                        <div className="flex flex-wrap gap-2">
                          {(professor.methods || []).map((method) => (
                            <Badge key={method} variant="outline">{method}</Badge>
                          ))}
                        </div>
                      </div>

                      <div className="flex items-center justify-between pt-4 border-t">
                        <div className="flex items-center space-x-6 text-sm text-gray-600 dark:text-gray-400">
                          <div className="flex items-center space-x-1">
                            <Users className="h-4 w-4" />
                            <span>{professor.acceptingStudents ? 'Accepting Students' : 'Not Accepting'}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <BookOpen className="h-4 w-4" />
                            <span>Profile: {professor.profileCompleteness}% complete</span>
                          </div>
                        </div>
                       
                        <div className="flex space-x-2">
                          <Button variant="outline" size="sm">
                            <MessageSquare className="h-4 w-4 mr-2" />
                            Message
                          </Button>
                          <Button size="sm">
                            <ExternalLink className="h-4 w-4 mr-2" />
                            View Profile
                          </Button>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </>
          )}
        </div>
      </div>
    </div>
  )
}
