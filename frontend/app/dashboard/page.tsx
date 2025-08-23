'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { 
  BookOpen, 
  Users, 
  MessageSquare, 
  TrendingUp, 
  Star, 
  MapPin, 
  Clock,
  Bell,
  Settings,
  Plus,
  Search,
  Filter
} from 'lucide-react'

// Mock data for demonstration
const MOCK_MATCHES = [
  {
    id: '1',
    type: 'professor',
    name: 'Dr. Sarah Chen',
    title: 'Associate Professor',
    institution: 'MIT',
    department: 'Computer Science',
    matchScore: 95,
    researchAreas: ['Machine Learning', 'NLP', 'Computer Vision'],
    location: 'Cambridge, MA',
    remote: 'Hybrid',
    lastActive: '2 days ago'
  },
  {
    id: '2',
    type: 'project',
    name: 'Advanced Language Model Development',
    professor: 'Dr. Sarah Chen',
    institution: 'MIT',
    matchScore: 92,
    researchAreas: ['NLP', 'Machine Learning'],
    hoursPerWeek: 20,
    compensation: 'Stipend',
    lastActive: '1 week ago'
  },
  {
    id: '3',
    type: 'professor',
    name: 'Dr. Michael Rodriguez',
    title: 'Assistant Professor',
    institution: 'Stanford',
    department: 'Electrical Engineering',
    matchScore: 87,
    researchAreas: ['Robotics', 'Control Systems', 'AI'],
    location: 'Stanford, CA',
    remote: 'On-site',
    lastActive: '3 days ago'
  }
]

const MOCK_ACTIVITY = [
  {
    id: '1',
    type: 'message',
    title: 'New message from Dr. Sarah Chen',
    description: 'Regarding your application for the NLP project',
    time: '2 hours ago',
    unread: true
  },
  {
    id: '2',
    type: 'match',
    title: 'New match found',
    description: 'Dr. Emily Watson at UC Berkeley (87% match)',
    time: '1 day ago',
    unread: false
  },
  {
    id: '3',
    type: 'application',
    title: 'Application status updated',
    description: 'Your application to MIT Robotics Lab is under review',
    time: '3 days ago',
    unread: false
  }
]

const MOCK_STATS = {
  totalMatches: 15,
  newMessages: 3,
  applicationsSent: 8,
  profileViews: 24,
  profileCompleteness: 85
}

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<'overview' | 'matches' | 'activity' | 'applications'>('overview')

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

  const renderOverview = () => (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Matches</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{MOCK_STATS.totalMatches}</div>
            <p className="text-xs text-muted-foreground">
              +2 from last week
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">New Messages</CardTitle>
            <MessageSquare className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{MOCK_STATS.newMessages}</div>
            <p className="text-xs text-muted-foreground">
              +1 from yesterday
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Applications</CardTitle>
            <BookOpen className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{MOCK_STATS.applicationsSent}</div>
            <p className="text-xs text-muted-foreground">
              +3 this month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Profile Views</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{MOCK_STATS.profileViews}</div>
            <p className="text-xs text-muted-foreground">
              +8 this week
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Profile Completeness */}
      <Card>
        <CardHeader>
          <CardTitle>Profile Completeness</CardTitle>
          <CardDescription>
            Complete your profile to get better matches
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="flex justify-between text-sm">
              <span>Profile Progress</span>
              <span>{MOCK_STATS.profileCompleteness}%</span>
            </div>
            <Progress value={MOCK_STATS.profileCompleteness} className="h-2" />
            <Button size="sm" className="bg-research-600 hover:bg-research-700">
              <Settings className="h-4 w-4 mr-2" />
              Complete Profile
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>
            Common tasks to help you get started
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Search className="h-6 w-6" />
              <span>Search Opportunities</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Plus className="h-6 w-6" />
              <span>Create Project</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <MessageSquare className="h-6 w-6" />
              <span>View Messages</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  const renderMatches = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Your Matches</h2>
        <Button variant="outline" size="sm">
          <Filter className="h-4 w-4 mr-2" />
          Filter
        </Button>
      </div>

      {MOCK_MATCHES.map((match) => (
        <Card key={match.id} className="hover:shadow-lg transition-shadow">
          <CardHeader>
            <div className="flex justify-between items-start">
              <div>
                <CardTitle className="text-xl">
                  {match.type === 'professor' ? match.name : match.name}
                </CardTitle>
                <CardDescription>
                  {match.type === 'professor' 
                    ? `${match.title} • ${match.department} • ${match.institution}`
                    : `${match.professor} • ${match.institution}`
                  }
                </CardDescription>
              </div>
              <div className="text-right">
                <Badge className={`${getMatchStrengthColor(match.matchScore)}`}>
                  {getMatchStrengthLabel(match.matchScore)}
                </Badge>
                <div className="text-2xl font-bold text-research-600 mt-1">
                  {match.matchScore}%
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-medium mb-2">Research Areas</h4>
                <div className="flex flex-wrap gap-2">
                  {match.researchAreas.map((area) => (
                    <Badge key={area} variant="secondary">{area}</Badge>
                  ))}
                </div>
              </div>

              <div className="flex items-center justify-between pt-4 border-t">
                <div className="flex items-center space-x-6 text-sm text-gray-600 dark:text-gray-400">
                  {match.type === 'professor' ? (
                    <>
                      <div className="flex items-center space-x-1">
                        <MapPin className="h-4 w-4" />
                        <span>{match.location}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Clock className="h-4 w-4" />
                        <span>{match.remote}</span>
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="flex items-center space-x-1">
                        <Clock className="h-4 w-4" />
                        <span>{match.hoursPerWeek} hrs/week</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Star className="h-4 w-4" />
                        <span>{match.compensation}</span>
                      </div>
                    </>
                  )}
                  <div className="flex items-center space-x-1">
                    <Clock className="h-4 w-4" />
                    <span>{match.lastActive}</span>
                  </div>
                </div>
                
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm">
                    <MessageSquare className="h-4 w-4 mr-2" />
                    Message
                  </Button>
                  <Button size="sm">
                    <BookOpen className="h-4 w-4 mr-2" />
                    View Details
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )

  const renderActivity = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Recent Activity</h2>
        <Button variant="outline" size="sm">
          <Bell className="h-4 w-4 mr-2" />
          Mark All Read
        </Button>
      </div>

      <div className="space-y-4">
        {MOCK_ACTIVITY.map((activity) => (
          <Card key={activity.id} className={activity.unread ? 'border-l-4 border-l-research-500' : ''}>
            <CardContent className="pt-6">
              <div className="flex items-start space-x-4">
                <div className={`w-3 h-3 rounded-full mt-2 ${activity.unread ? 'bg-research-500' : 'bg-gray-300'}`} />
                <div className="flex-1">
                  <h4 className="font-medium">{activity.title}</h4>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{activity.description}</p>
                  <p className="text-xs text-gray-500 mt-2">{activity.time}</p>
                </div>
                {activity.unread && (
                  <Badge variant="secondary" className="text-xs">New</Badge>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )

  const renderApplications = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-xl font-semibold">Your Applications</h2>
        <Button size="sm">
          <Plus className="h-4 w-4 mr-2" />
          New Application
        </Button>
      </div>

      <Card>
        <CardContent className="pt-6">
          <div className="text-center py-12">
            <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium mb-2">No applications yet</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              Start applying to research opportunities to see your applications here
            </p>
            <Button>
              <Search className="h-4 w-4 mr-2" />
              Find Opportunities
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Welcome back! Here's what's happening with your research matches.
          </p>
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 mb-8 bg-white dark:bg-gray-800 rounded-lg p-1">
          {[
            { id: 'overview', label: 'Overview', icon: TrendingUp },
            { id: 'matches', label: 'Matches', icon: Users },
            { id: 'activity', label: 'Activity', icon: Bell },
            { id: 'applications', label: 'Applications', icon: BookOpen }
          ].map((tab) => (
            <Button
              key={tab.id}
              variant={activeTab === tab.id ? 'default' : 'ghost'}
              onClick={() => setActiveTab(tab.id as any)}
              className="flex items-center space-x-2"
            >
              <tab.icon className="h-4 w-4" />
              <span>{tab.label}</span>
            </Button>
          ))}
        </div>

        {/* Tab Content */}
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'matches' && renderMatches()}
        {activeTab === 'activity' && renderActivity()}
        {activeTab === 'applications' && renderApplications()}
      </div>
    </div>
  )
}
