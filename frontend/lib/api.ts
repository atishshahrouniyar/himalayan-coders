import { 
  StudentProfile, 
  ProfessorProfile, 
  Match 
} from '@/types'

// API Response types
interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string,
    public fieldErrors?: Record<string, string[]>
  ) {
    super(message)
    this.name = 'ApiError'
  }
}


async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new ApiError(
      errorData.message || `HTTP error! status: ${response.status}`,
      response.status,
      errorData.code,
      errorData.fieldErrors
    )
  }
  
  return response.json()
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  }
  
  const response = await fetch(url, { ...defaultOptions, ...options })
  return handleResponse<T>(response)
}

// Student Profile API
export const studentApi = {
  // Get all students
  getAll: (filters: {
    query?: string
    department?: string
    level?: string
    tags?: string[]
  } = {}) => {
    const params = new URLSearchParams()
    if (filters?.query) params.append('q', filters.query)
    if (filters?.department) params.append('department', filters.department)
    if (filters?.level) params.append('degree_level', filters.level)
    if (filters?.tags) {
      filters.tags.forEach(tag => params.append('interests', tag))
    }
    
    return apiRequest<PaginatedResponse<StudentProfile>>(`/students/?${params.toString()}`)
  },

  // Get student by ID
  getById: (id: string) => 
    apiRequest<StudentProfile>(`/students/${id}/`),

  // Create new student profile
  create: (data: Partial<StudentProfile>) =>
    apiRequest<StudentProfile>('/students/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Update student profile
  update: (id: string, data: Partial<StudentProfile>) =>
    apiRequest<StudentProfile>(`/students/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  // Delete student profile
  delete: (id: string) =>
    apiRequest<void>(`/students/${id}/`, {
      method: 'DELETE',
    }),

  // Get matching status
  getMatchingStatus: (id: string) =>
    apiRequest<{
      status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'not_found'
      progress: number
      started_at: string | null
      completed_at: string | null
      error: string | null
    }>(`/students/${id}/matching_status/`),

  // Search students
  search: (filters: {
    query?: string
    department?: string
    level?: string
    tags?: string[]
  } = {}) => {
    const params = new URLSearchParams()
    if (filters.query) params.append('q', filters.query)
    if (filters.department) params.append('department', filters.department)
    if (filters.level) params.append('degree_level', filters.level)
    if (filters.tags) {
      filters.tags.forEach(tag => params.append('interests', tag))
    }
    
    return apiRequest<StudentProfile[]>(`/students/search/?${params.toString()}`)
  },
}

// Professor Profile API
export const professorApi = {
  // Get all professors
  getAll: (filters: {
    query?: string
    tags?: string[]
    department?: string
    acceptingStudents?: boolean
  } = {}) => {
    const params = new URLSearchParams()
    if (filters.query) params.append('query', filters.query)
    if (filters.tags?.length) params.append('tags', filters.tags.join(','))
    if (filters.department) params.append('department', filters.department)
    if (filters.acceptingStudents !== undefined) params.append('accepting_students', filters.acceptingStudents.toString())
    
    return apiRequest<PaginatedResponse<ProfessorProfile>>(`/professors/?${params.toString()}`)
  },

  // Get professor by ID
  getById: (id: string) =>
    apiRequest<ProfessorProfile>(`/professors/${id}/`),

  // Create professor
  create: (data: Partial<ProfessorProfile>) =>
    apiRequest<ProfessorProfile>('/professors/', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  // Update professor
  update: (id: string, data: Partial<ProfessorProfile>) =>
    apiRequest<ProfessorProfile>(`/professors/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),

  // Delete professor
  delete: (id: string) =>
    apiRequest<void>(`/professors/${id}/`, {
      method: 'DELETE'
    }),

  // Search professors
  search: (filters: {
    query?: string
    tags?: string[]
    department?: string
    acceptingStudents?: boolean
  } = {}) => {
    const params = new URLSearchParams()
    if (filters.query) params.append('query', filters.query)
    if (filters.tags?.length) params.append('tags', filters.tags.join(','))
    if (filters.department) params.append('department', filters.department)
    if (filters.acceptingStudents !== undefined) params.append('accepting_students', filters.acceptingStudents.toString())
    
    return apiRequest<ProfessorProfile[]>(`/professors/search/?${params.toString()}`)
  }
}

export const matchApi = {
  // Get all matches
  getAll: (filters: {
    studentId?: string
    professorId?: string
    minScore?: number
  } = {}) => {
    const params = new URLSearchParams()
    if (filters?.studentId) params.append('student_id', filters.studentId)
    if (filters?.professorId) params.append('professor_id', filters.professorId)
    if (filters?.minScore) params.append('min_score', filters.minScore.toString())
    
    return apiRequest<PaginatedResponse<Match>>(`/matches/?${params.toString()}`)
  },

  // Get match by ID
  getById: (id: string) =>
    apiRequest<Match>(`/matches/${id}/`),

  // Create match
  create: (data: Partial<Match>) =>
    apiRequest<Match>('/matches/', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  // Update match
  update: (id: string, data: Partial<Match>) =>
    apiRequest<Match>(`/matches/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data)
    }),

  // Delete match
  delete: (id: string) =>
    apiRequest<void>(`/matches/${id}/`, {
      method: 'DELETE'
    }),

  // Generate AI matches
  generateMatches: (studentId: string, useAi: boolean = true) => {
    const params = new URLSearchParams()
    params.append('student_id', studentId)
    params.append('use_ai', useAi.toString())
    
    return apiRequest<Match[]>('/matches/generate/', {
      method: 'POST',
      body: JSON.stringify({ student_id: studentId, use_ai: useAi })
    })
  }
}

export const searchApi = {
  // Global search across all entities
  global: (query: string, entityType: 'students' | 'professors' | 'all' = 'all') => {
    const params = new URLSearchParams()
    params.append('query', query)
    params.append('type', entityType)
    
    return apiRequest<{
      students: StudentProfile[]
      professors: ProfessorProfile[]
    }>(`/search/?${params.toString()}`)
  }
}

// Utility function to check if API is available
export const checkApiHealth = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_BASE_URL}/students/`)
    return response.ok
  } catch (error) {
    console.error('API health check failed:', error)
    return false
  }
}

// Export the custom ApiError class
export { ApiError }
