import { 
  StudentProfile, 
  ProfessorProfile, 
  ResearchProject, 
  Match, 
  SearchFilters,
  ApiResponse
} from '@/types'

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
): Promise<ApiResponse<T>> {
  const url = `${API_BASE_URL}${endpoint}`
  
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  }
  
  const response = await fetch(url, { ...defaultOptions, ...options })
  return handleResponse<ApiResponse<T>>(response)
}

// Student Profile API
export const studentApi = {
  // Get all students
  getAll: (filters?: SearchFilters) => {
    const params = new URLSearchParams()
    if (filters?.query) params.append('q', filters.query)
    if (filters?.department) params.append('department', filters.department)
    if (filters?.level) params.append('degree_level', filters.level)
    if (filters?.tags) {
      filters.tags.forEach(tag => params.append('interests', tag))
    }
    
    return apiRequest<StudentProfile[]>(`/students/?${params.toString()}`)
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

  // Search students
  search: (filters: SearchFilters) => {
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
  getAll: (filters?: SearchFilters) => {
    const params = new URLSearchParams()
    if (filters?.query) params.append('q', filters.query)
    if (filters?.department) params.append('department', filters.department)
    if (filters?.tags) {
      filters.tags.forEach(tag => params.append('research_areas', tag))
    }
    
    return apiRequest<ProfessorProfile[]>(`/professors/?${params.toString()}`)
  },

  // Get professor by ID
  getById: (id: string) => 
    apiRequest<ProfessorProfile>(`/professors/${id}/`),

  // Create new professor profile
  create: (data: Partial<ProfessorProfile>) =>
    apiRequest<ProfessorProfile>('/professors/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Update professor profile
  update: (id: string, data: Partial<ProfessorProfile>) =>
    apiRequest<ProfessorProfile>(`/professors/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  // Delete professor profile
  delete: (id: string) =>
    apiRequest<void>(`/professors/${id}/`, {
      method: 'DELETE',
    }),

  // Search professors
  search: (filters: SearchFilters) => {
    const params = new URLSearchParams()
    if (filters.query) params.append('q', filters.query)
    if (filters.department) params.append('department', filters.department)
    if (filters.tags) {
      filters.tags.forEach(tag => params.append('research_areas', tag))
    }
    
    return apiRequest<ProfessorProfile[]>(`/professors/search/?${params.toString()}`)
  },
}

// Research Project API
export const projectApi = {
  // Get all projects
  getAll: (filters?: SearchFilters) => {
    const params = new URLSearchParams()
    if (filters?.query) params.append('q', filters.query)
    if (filters?.tags) {
      filters.tags.forEach(tag => params.append('research_areas', tag))
    }
    if (filters?.compensation) params.append('compensation', filters.compensation)
    if (filters?.remote !== undefined) params.append('location', filters.remote ? 'Remote' : 'On-site')
    if (filters?.availability) params.append('min_hours', filters.availability.toString())
    
    return apiRequest<ResearchProject[]>(`/projects/?${params.toString()}`)
  },

  // Get project by ID
  getById: (id: string) => 
    apiRequest<ResearchProject>(`/projects/${id}/`),

  // Create new project
  create: (data: Partial<ResearchProject>) =>
    apiRequest<ResearchProject>('/projects/', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Update project
  update: (id: string, data: Partial<ResearchProject>) =>
    apiRequest<ResearchProject>(`/projects/${id}/`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  // Delete project
  delete: (id: string) =>
    apiRequest<void>(`/projects/${id}/`, {
      method: 'DELETE',
    }),

  // Search projects
  search: (filters: SearchFilters) => {
    const params = new URLSearchParams()
    if (filters.query) params.append('q', filters.query)
    if (filters.tags) {
      filters.tags.forEach(tag => params.append('research_areas', tag))
    }
    if (filters.compensation) params.append('compensation', filters.compensation)
    if (filters.remote !== undefined) params.append('location', filters.remote ? 'Remote' : 'On-site')
    if (filters.availability) params.append('min_hours', filters.availability.toString())
    
    return apiRequest<ResearchProject[]>(`/projects/search/?${params.toString()}`)
  },
}

// Match API
export const matchApi = {
  // Get all matches
  getAll: () => 
    apiRequest<Match[]>('/matches/'),

  // Get match by ID
  getById: (id: string) => 
    apiRequest<Match>(`/matches/${id}/`),

  // Generate matches for a student
  generateMatches: (studentId: string, matchType: 'professor' | 'project' = 'professor') =>
    apiRequest<Match[]>('/matches/generate_matches/', {
      method: 'POST',
      body: JSON.stringify({
        student_id: studentId,
        match_type: matchType,
      }),
    }),

  // Get matches for a student
  getStudentMatches: (studentId: string) => {
    const params = new URLSearchParams()
    params.append('student', studentId)
    return apiRequest<Match[]>(`/matches/?${params.toString()}`)
  },
}

// Search API
export const searchApi = {
  // Global search across all entities
  global: (query: string, entityType: 'students' | 'professors' | 'projects' | 'all' = 'all') => {
    const params = new URLSearchParams()
    params.append('q', query)
    params.append('type', entityType)
    
    return apiRequest<{
      students: StudentProfile[]
      professors: ProfessorProfile[]
      projects: ResearchProject[]
    }>(`/search/global/?${params.toString()}`)
  },
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
