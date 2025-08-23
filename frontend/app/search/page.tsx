'use client'

import { useState } from 'react'
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
  ExternalLink
} from 'lucide-react'
import { RESEARCH_AREAS, METHODS_TECHNIQUES, DEGREE_LEVELS, COMPENSATION_TYPES } from '@/lib/constants'

// Mock data for demonstration
const MOCK_PROFESSORS = [
  {
    id: '1',
    name: 'Dr. Sarah Chen',
    title: 'Associate Professor',
    department: 'Computer Science',
    institution: 'MIT',
    researchAreas: ['Machine Learning', 'NLP', 'Computer Vision'],
    methods: ['Deep Learning', 'Transformers', 'Neural Networks'],
    acceptingStudents: true,
    preferredDegreeLevels: ['MS', 'PhD'],
    matchScore: 95,
    location: 'Cambridge, MA',
    remote: 'Hybrid'
  },
  {
    id: '2',
    name: 'Dr. Michael Rodriguez',
    title: 'Assistant Professor',
    department: 'Electrical Engineering',
    institution: 'Stanford',
    researchAreas: ['Robotics', 'Control Systems', 'AI'],
    methods: ['Reinforcement Learning', 'Control Theory', 'Optimization'],
    acceptingStudents: true,
    preferredDegreeLevels: ['BS', 'MS', 'PhD'],
    matchScore: 87,
    location: 'Stanford, CA',
    remote: 'On-site'
  },
  {
    id: '3',
    name: 'Dr. Emily Watson',
    title: 'Professor',
    department: 'Bioinformatics',
    institution: 'UC Berkeley',
    researchAreas: ['Bioinformatics', 'Genomics', 'Data Science'],
    methods: ['Statistical Analysis', 'Machine Learning', 'Data Mining'],
    acceptingStudents: false,
    preferredDegreeLevels: ['PhD'],
    matchScore: 78,
    location: 'Berkeley, CA',
    remote: 'Remote'
  }
]

const MOCK_PROJECTS = [
  {
    id: '1',
    title: 'Advanced Language Model Development',
    summary: 'Developing next-generation language models for scientific literature analysis',
    researchAreas: ['NLP', 'Machine Learning'],
    techniques: ['Transformers', 'Deep Learning', 'Natural Language Processing'],
    desiredSkills: ['Python', 'PyTorch', 'NLP'],
    hoursPerWeek: 20,
    compensation: 'Stipend',
    location: 'Remote',
    professor: 'Dr. Sarah Chen',
    institution: 'MIT',
    matchScore: 92
  },
  {
    id: '2',
    title: 'Autonomous Robot Navigation',
    summary: 'Building intelligent navigation systems for autonomous robots in complex environments',
    researchAreas: ['Robotics', 'AI', 'Control Systems'],
    techniques: ['Reinforcement Learning', 'Computer Vision', 'Path Planning'],
    desiredSkills: ['Python', 'C++', 'ROS', 'Machine Learning'],
    hoursPerWeek: 15,
    compensation: 'Credit',
    location: 'On-site',
    professor: 'Dr. Michael Rodriguez',
    institution: 'Stanford',
    matchScore: 88
  }
]

export default function SearchPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedAreas, setSelectedAreas] = useState<string[]>([])
  const [selectedMethods, setSelectedMethods] = useState<string[]>([])
  const [selectedDegreeLevel, setSelectedDegreeLevel] = useState('')
  const [selectedCompensation, setSelectedCompensation] = useState('')
  const [searchType, setSearchType] = useState<'professors' | 'projects'>('professors')
  const [showFilters, setShowFilters] = useState(false)

  const filteredProfessors = MOCK_PROFESSORS.filter(prof => {
    if (searchQuery && !prof.name.toLowerCase().includes(searchQuery.toLowerCase()) && 
        !prof.researchAreas.some(area => area.toLowerCase().includes(searchQuery.toLowerCase()))) {
      return false
    }
    if (selectedAreas.length > 0 && !selectedAreas.some(area => prof.researchAreas.includes(area))) {
      return false
    }
    if (selectedMethods.length > 0 && !selectedMethods.some(method => prof.methods.includes(method))) {
      return false
    }
    if (selectedDegreeLevel && !prof.preferredDegreeLevels.includes(selectedDegreeLevel)) {
      return false
    }
    return true
  })

  const filteredProjects = MOCK_PROJECTS.filter(project => {
    if (searchQuery && !project.title.toLowerCase().includes(searchQuery.toLowerCase()) && 
        !project.researchAreas.some(area => area.toLowerCase().includes(searchQuery.toLowerCase()))) {
      return false
    }
    if (selectedAreas.length > 0 && !selectedAreas.some(area => project.researchAreas.includes(area))) {
      return false
    }
    if (selectedMethods.length > 0 && !selectedMethods.some(method => project.techniques.includes(method))) {
      return false
    }
    if (selectedCompensation && project.compensation !== selectedCompensation) {
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
            Find professors and research projects that match your interests and skills
          </p>
        </div>

        {/* Search Type Toggle */}
        <div className="flex space-x-2 mb-6">
          <Button
            variant={searchType === 'professors' ? 'default' : 'outline'}
            onClick={() => setSearchType('professors')}
            className="flex items-center space-x-2"
          >
            <Users className="h-4 w-4" />
            Professors
          </Button>
          <Button
            variant={searchType === 'projects' ? 'default' : 'outline'}
            onClick={() => setSearchType('projects')}
            className="flex items-center space-x-2"
          >
            <BookOpen className="h-4 w-4" />
            Projects
          </Button>
        </div>

        {/* Search Bar and Filters */}
        <div className="mb-8">
          <div className="flex flex-col lg:flex-row gap-4 mb-4">
            <div className="flex-1 relative">
              <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder={`Search ${searchType}...`}
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <Button
              variant="outline"
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center space-x-2"
            >
              <Filter className="h-4 w-4" />
              Filters
            </Button>
          </div>

          {/* Filters Panel */}
          {showFilters && (
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
                      value={selectedDegreeLevel}
                      onChange={(e) => setSelectedDegreeLevel(e.target.value)}
                    >
                      <option value="">Any Level</option>
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
                      onChange={(e) => setSelectedCompensation(e.target.value)}
                    >
                      <option value="">Any Type</option>
                      {COMPENSATION_TYPES.map((type) => (
                        <option key={type} value={type}>{type}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Results */}
        <div className="space-y-6">
          {searchType === 'professors' ? (
            <>
              <h2 className="text-xl font-semibold">
                Professors ({filteredProfessors.length} results)
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
                        <Badge className={`${getMatchStrengthColor(professor.matchScore)}`}>
                          {getMatchStrengthLabel(professor.matchScore)}
                        </Badge>
                        <div className="text-2xl font-bold text-research-600 mt-1">
                          {professor.matchScore}%
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div>
                        <h4 className="font-medium mb-2">Research Areas</h4>
                        <div className="flex flex-wrap gap-2">
                          {professor.researchAreas.map((area) => (
                            <Badge key={area} variant="secondary">{area}</Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div>
                        <h4 className="font-medium mb-2">Methods & Techniques</h4>
                        <div className="flex flex-wrap gap-2">
                          {professor.methods.map((method) => (
                            <Badge key={method} variant="outline">{method}</Badge>
                          ))}
                        </div>
                      </div>

                      <div className="flex items-center justify-between pt-4 border-t">
                        <div className="flex items-center space-x-6 text-sm text-gray-600 dark:text-gray-400">
                          <div className="flex items-center space-x-1">
                            <MapPin className="h-4 w-4" />
                            <span>{professor.location}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <Clock className="h-4 w-4" />
                            <span>{professor.remote}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <Users className="h-4 w-4" />
                            <span>{professor.acceptingStudents ? 'Accepting Students' : 'Not Accepting'}</span>
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
          ) : (
            <>
              <h2 className="text-xl font-semibold">
                Research Projects ({filteredProjects.length} results)
              </h2>
              {filteredProjects.map((project) => (
                <Card key={project.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="text-xl">{project.title}</CardTitle>
                        <CardDescription>
                          {project.professor} • {project.institution}
                        </CardDescription>
                      </div>
                      <div className="text-right">
                        <Badge className={`${getMatchStrengthColor(project.matchScore)}`}>
                          {getMatchStrengthLabel(project.matchScore)}
                        </Badge>
                        <div className="text-2xl font-bold text-research-600 mt-1">
                          {project.matchScore}%
                        </div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <p className="text-gray-600 dark:text-gray-400">{project.summary}</p>
                      
                      <div>
                        <h4 className="font-medium mb-2">Research Areas</h4>
                        <div className="flex flex-wrap gap-2">
                          {project.researchAreas.map((area) => (
                            <Badge key={area} variant="secondary">{area}</Badge>
                          ))}
                        </div>
                      </div>
                      
                      <div>
                        <h4 className="font-medium mb-2">Required Skills</h4>
                        <div className="flex flex-wrap gap-2">
                          {project.desiredSkills.map((skill) => (
                            <Badge key={skill} variant="outline">{skill}</Badge>
                          ))}
                        </div>
                      </div>

                      <div className="flex items-center justify-between pt-4 border-t">
                        <div className="flex items-center space-x-6 text-sm text-gray-600 dark:text-gray-400">
                          <div className="flex items-center space-x-1">
                            <Clock className="h-4 w-4" />
                            <span>{project.hoursPerWeek} hrs/week</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <MapPin className="h-4 w-4" />
                            <span>{project.location}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <Star className="h-4 w-4" />
                            <span>{project.compensation}</span>
                          </div>
                        </div>
                        
                        <div className="flex space-x-2">
                          <Button variant="outline" size="sm">
                            <MessageSquare className="h-4 w-4 mr-2" />
                            Contact
                          </Button>
                          <Button size="sm">
                            <ExternalLink className="h-4 w-4 mr-2" />
                            Apply
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
