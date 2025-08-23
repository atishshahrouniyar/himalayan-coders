import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  studentApi, 
  professorApi, 
  matchApi, 
  searchApi 
} from './api'
import { 
  StudentProfile, 
  ProfessorProfile, 
  Match 
} from '@/types'

// Query keys
export const queryKeys = {
  students: ['students'] as const,
  student: (id: string) => ['students', id] as const,
  professors: ['professors'] as const,
  professor: (id: string) => ['professors', id] as const,
  matches: ['matches'] as const,
  match: (id: string) => ['matches', id] as const,
  search: ['search'] as const,
} as const

// Student hooks
export const useStudents = (filters?: {
  query?: string
  department?: string
  level?: string
  tags?: string[]
}) => {
  return useQuery({
    queryKey: [...queryKeys.students, filters],
    queryFn: () => studentApi.getAll(filters),
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

export const useSearchStudents = (filters: {
  query?: string
  department?: string
  level?: string
  tags?: string[]
}) => {
  return useQuery({
    queryKey: [...queryKeys.students, 'search', filters],
    queryFn: () => studentApi.search(filters),
  })
}

// Professor hooks
export const useProfessors = (filters?: {
  query?: string
  tags?: string[]
  department?: string
  acceptingStudents?: boolean
}) => {
  return useQuery({
    queryKey: [...queryKeys.professors, filters],
    queryFn: () => professorApi.getAll(filters),
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

export const useSearchProfessors = (filters: {
  query?: string
  tags?: string[]
  department?: string
  acceptingStudents?: boolean
}) => {
  return useQuery({
    queryKey: [...queryKeys.professors, 'search', filters],
    queryFn: () => professorApi.search(filters),
  })
}

// Match hooks
export const useMatches = (filters?: {
  studentId?: string
  professorId?: string
  minScore?: number
}) => {
  return useQuery({
    queryKey: [...queryKeys.matches, filters],
    queryFn: () => matchApi.getAll(filters),
  })
}

export const useMatch = (id: string) => {
  return useQuery({
    queryKey: queryKeys.match(id),
    queryFn: () => matchApi.getById(id),
    enabled: !!id,
  })
}

export const useCreateMatch = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: Partial<Match>) => matchApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.matches })
    },
  })
}

export const useUpdateMatch = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Match> }) =>
      matchApi.update(id, data),
    onSuccess: (_, { id }) => {
      queryClient.invalidateQueries({ queryKey: queryKeys.matches })
      queryClient.invalidateQueries({ queryKey: queryKeys.match(id) })
    },
  })
}

export const useDeleteMatch = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => matchApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.matches })
    },
  })
}

export const useGenerateMatches = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ studentId, useAi }: { studentId: string; useAi?: boolean }) =>
      matchApi.generateMatches(studentId, useAi),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.matches })
    },
  })
}

// Search hooks
export const useGlobalSearch = (query: string, entityType: 'students' | 'professors' | 'all' = 'all') => {
  return useQuery({
    queryKey: [...queryKeys.search, query, entityType],
    queryFn: () => searchApi.global(query, entityType),
    enabled: !!query.trim(),
  })
}
