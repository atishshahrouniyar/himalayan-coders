import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  studentApi, 
  professorApi, 
  projectApi, 
  matchApi, 
  searchApi,
  ApiError 
} from './api'
import { 
  StudentProfile, 
  ProfessorProfile, 
  ResearchProject, 
  Match, 
  SearchFilters 
} from '@/types'

// Query keys
export const queryKeys = {
  students: ['students'] as const,
  student: (id: string) => ['students', id] as const,
  professors: ['professors'] as const,
  professor: (id: string) => ['professors', id] as const,
  projects: ['projects'] as const,
  project: (id: string) => ['projects', id] as const,
  matches: ['matches'] as const,
  match: (id: string) => ['matches', id] as const,
  search: (query: string, type: string) => ['search', query, type] as const,
}

// Student Profile Hooks
export const useStudents = (filters?: SearchFilters) => {
  return useQuery({
    queryKey: [...queryKeys.students, filters],
    queryFn: () => studentApi.getAll(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export const useStudent = (id: string) => {
  return useQuery({
    queryKey: queryKeys.student(id),
    queryFn: () => studentApi.getById(id),
    enabled: !!id,
  })
}

export const useCreateStudent = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: Partial<StudentProfile>) => studentApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.students })
    },
  })
}

export const useUpdateStudent = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<StudentProfile> }) =>
      studentApi.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.students })
      queryClient.invalidateQueries({ queryKey: queryKeys.student(id) })
    },
  })
}

export const useDeleteStudent = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => studentApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.students })
    },
  })
}

export const useSearchStudents = (filters: SearchFilters) => {
  return useQuery({
    queryKey: [...queryKeys.students, 'search', filters],
    queryFn: () => studentApi.search(filters),
    enabled: !!filters.query || !!filters.department || !!filters.level || !!filters.tags?.length,
  })
}

// Professor Profile Hooks
export const useProfessors = (filters?: SearchFilters) => {
  return useQuery({
    queryKey: [...queryKeys.professors, filters],
    queryFn: () => professorApi.getAll(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export const useProfessor = (id: string) => {
  return useQuery({
    queryKey: queryKeys.professor(id),
    queryFn: () => professorApi.getById(id),
    enabled: !!id,
  })
}

export const useCreateProfessor = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: Partial<ProfessorProfile>) => professorApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.professors })
    },
  })
}

export const useUpdateProfessor = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<ProfessorProfile> }) =>
      professorApi.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.professors })
      queryClient.invalidateQueries({ queryKey: queryKeys.professor(id) })
    },
  })
}

export const useDeleteProfessor = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => professorApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.professors })
    },
  })
}

export const useSearchProfessors = (filters: SearchFilters) => {
  return useQuery({
    queryKey: [...queryKeys.professors, 'search', filters],
    queryFn: () => professorApi.search(filters),
    enabled: !!filters.query || !!filters.department || !!filters.tags?.length,
  })
}

// Research Project Hooks
export const useProjects = (filters?: SearchFilters) => {
  return useQuery({
    queryKey: [...queryKeys.projects, filters],
    queryFn: () => projectApi.getAll(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export const useProject = (id: string) => {
  return useQuery({
    queryKey: queryKeys.project(id),
    queryFn: () => projectApi.getById(id),
    enabled: !!id,
  })
}

export const useCreateProject = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (data: Partial<ResearchProject>) => projectApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.projects })
    },
  })
}

export const useUpdateProject = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<ResearchProject> }) =>
      projectApi.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.projects })
      queryClient.invalidateQueries({ queryKey: queryKeys.project(id) })
    },
  })
}

export const useDeleteProject = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: (id: string) => projectApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.projects })
    },
  })
}

export const useSearchProjects = (filters: SearchFilters) => {
  return useQuery({
    queryKey: [...queryKeys.projects, 'search', filters],
    queryFn: () => projectApi.search(filters),
    enabled: !!filters.query || !!filters.tags?.length || !!filters.compensation || filters.remote !== undefined || !!filters.availability,
  })
}

// Match Hooks
export const useMatches = () => {
  return useQuery({
    queryKey: queryKeys.matches,
    queryFn: () => matchApi.getAll(),
  })
}

export const useMatch = (id: string) => {
  return useQuery({
    queryKey: queryKeys.match(id),
    queryFn: () => matchApi.getById(id),
    enabled: !!id,
  })
}

export const useGenerateMatches = () => {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationFn: ({ studentId, matchType }: { studentId: string; matchType: 'professor' | 'project' }) =>
      matchApi.generateMatches(studentId, matchType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.matches })
    },
  })
}

export const useStudentMatches = (studentId: string) => {
  return useQuery({
    queryKey: [...queryKeys.matches, 'student', studentId],
    queryFn: () => matchApi.getStudentMatches(studentId),
    enabled: !!studentId,
  })
}

// Search Hooks
export const useGlobalSearch = (query: string, entityType: 'students' | 'professors' | 'projects' | 'all' = 'all') => {
  return useQuery({
    queryKey: queryKeys.search(query, entityType),
    queryFn: () => searchApi.global(query, entityType),
    enabled: !!query,
    staleTime: 2 * 60 * 1000, // 2 minutes
  })
}

// Utility hook for error handling
export const useApiError = (error: unknown) => {
  if (error instanceof ApiError) {
    return {
      message: error.message,
      status: error.status,
      code: error.code,
      fieldErrors: error.fieldErrors,
    }
  }
  
  return {
    message: error instanceof Error ? error.message : 'An unknown error occurred',
    status: 500,
  }
}
