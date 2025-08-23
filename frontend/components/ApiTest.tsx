'use client'

import React, { useState } from 'react'
import { useStudents, useProfessors, useCreateStudent } from '@/lib/hooks'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

export default function ApiTest() {
  const [activeTab, setActiveTab] = useState<'students' | 'professors'>('students')
  const [showCreateForm, setShowCreateForm] = useState(false)
  
  // API hooks
  const { data: studentsData, isLoading: studentsLoading, error: studentsError } = useStudents()
  const { data: professorsData, isLoading: professorsLoading, error: professorsError } = useProfessors()
  const createStudentMutation = useCreateStudent()
  
  // Error handling
  const studentsErrorInfo = studentsError
  const professorsErrorInfo = professorsError
  
  // Form state
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    university: '',
    department: '',
    degreeLevel: 'BS' as 'BS' | 'MS' | 'PhD' | 'Other',
    year: 2024,
    semester: 1,
    primaryInterests: [] as string[],
    hoursPerWeek: 10,
  })
  
  const handleCreateStudent = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await createStudentMutation.mutateAsync(formData)
      setShowCreateForm(false)
      setFormData({
        firstName: '',
        lastName: '',
        email: '',
        university: '',
        department: '',
        degreeLevel: 'BS',
        year: 2024,
        semester: 1,
        primaryInterests: [],
        hoursPerWeek: 10,
      })
    } catch (error) {
      console.error('Failed to create student:', error)
    }
  }
  
  const renderStudents = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Students</h3>
        <Button onClick={() => setShowCreateForm(true)}>Add Student</Button>
      </div>
      
      {studentsLoading && <p>Loading students...</p>}
      {studentsError && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <p className="text-red-600">Error: {studentsErrorInfo?.message || 'Unknown error'}</p>
          </CardContent>
        </Card>
      )}
      
      {studentsData && (
        <div className="grid gap-4">
          {(Array.isArray(studentsData) ? studentsData : studentsData.results || []).map((student: any) => (
            <Card key={student.id}>
              <CardHeader>
                <CardTitle>{student.firstName} {student.lastName}</CardTitle>
                <CardDescription>{student.university} - {student.department}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex gap-2 mb-2">
                  <Badge variant="secondary">{student.degreeLevel}</Badge>
                  <Badge variant="outline">Year {student.year}</Badge>
                </div>
                {student.primaryInterests.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {student.primaryInterests.map((interest: string, index: number) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {interest}
                      </Badge>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
  
  const renderProfessors = () => (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Professors</h3>
      
      {professorsLoading && <p>Loading professors...</p>}
      {professorsError && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <p className="text-red-600">Error: {professorsErrorInfo?.message || 'Unknown error'}</p>
          </CardContent>
        </Card>
      )}
      
      {professorsData && (
        <div className="grid gap-4">
          {(Array.isArray(professorsData) ? professorsData : professorsData.results || []).map((professor: any) => (
            <Card key={professor.id}>
              <CardHeader>
                <CardTitle>Dr. {professor.name}</CardTitle>
                <CardDescription>{professor.title} at {professor.institution}</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600 mb-2">{professor.department}</p>
                {professor.researchAreas.length > 0 && (
                  <div className="flex flex-wrap gap-1">
                    {professor.researchAreas.map((area: string, index: number) => (
                      <Badge key={index} variant="outline" className="text-xs">
                        {area}
                      </Badge>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
  

  
  return (
    <div className="container mx-auto p-6 max-w-4xl">
      <Card>
        <CardHeader>
          <CardTitle>API Integration Test</CardTitle>
          <CardDescription>
            Test the integration between frontend and backend APIs
          </CardDescription>
        </CardHeader>
        <CardContent>
          {/* Tab Navigation */}
          <div className="flex space-x-1 mb-6">
            <Button
              variant={activeTab === 'students' ? 'default' : 'outline'}
              onClick={() => setActiveTab('students')}
            >
              Students
            </Button>
            <Button
              variant={activeTab === 'professors' ? 'default' : 'outline'}
              onClick={() => setActiveTab('professors')}
            >
              Professors
            </Button>

          </div>
          
          {/* Content */}
          {activeTab === 'students' && renderStudents()}
          {activeTab === 'professors' && renderProfessors()}
        </CardContent>
      </Card>
      
      {/* Create Student Form Modal */}
      {showCreateForm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>Create New Student</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleCreateStudent} className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="firstName">First Name</Label>
                    <Input
                      id="firstName"
                      value={formData.firstName}
                      onChange={(e) => setFormData({ ...formData, firstName: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="lastName">Last Name</Label>
                    <Input
                      id="lastName"
                      value={formData.lastName}
                      onChange={(e) => setFormData({ ...formData, lastName: e.target.value })}
                      required
                    />
                  </div>
                </div>
                
                <div>
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="university">University</Label>
                    <Input
                      id="university"
                      value={formData.university}
                      onChange={(e) => setFormData({ ...formData, university: e.target.value })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="department">Department</Label>
                    <Input
                      id="department"
                      value={formData.department}
                      onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                      required
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="degreeLevel">Degree Level</Label>
                    <Select
                      value={formData.degreeLevel}
                      onValueChange={(value: 'BS' | 'MS' | 'PhD' | 'Other') => 
                        setFormData({ ...formData, degreeLevel: value })
                      }
                    >
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="BS">BS</SelectItem>
                        <SelectItem value="MS">MS</SelectItem>
                        <SelectItem value="PhD">PhD</SelectItem>
                        <SelectItem value="Other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="year">Year</Label>
                    <Input
                      id="year"
                      type="number"
                      value={formData.year}
                      onChange={(e) => setFormData({ ...formData, year: parseInt(e.target.value) })}
                      required
                    />
                  </div>
                  <div>
                    <Label htmlFor="hoursPerWeek">Hours/Week</Label>
                    <Input
                      id="hoursPerWeek"
                      type="number"
                      value={formData.hoursPerWeek}
                      onChange={(e) => setFormData({ ...formData, hoursPerWeek: parseInt(e.target.value) })}
                      required
                    />
                  </div>
                </div>
                
                <div className="flex gap-2">
                  <Button type="submit" disabled={createStudentMutation.isPending}>
                    {createStudentMutation.isPending ? 'Creating...' : 'Create Student'}
                  </Button>
                  <Button type="button" variant="outline" onClick={() => setShowCreateForm(false)}>
                    Cancel
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
