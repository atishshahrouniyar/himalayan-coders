export interface User {
  id: string;
  email: string;
  name: string;
  role: 'student' | 'professor' | 'admin';
  createdAt: Date;
  updatedAt: Date;
}

export interface StudentProfile {
  id: string;
  userId: string;
  firstName: string;
  lastName: string;
  preferredName?: string;
  email: string;
  university: string;
  department: string;
  degreeLevel: 'BS' | 'MS' | 'PhD' | 'Other';
  year: number;
  semester: number;
  gpa?: number;
  graduationTarget?: string;
  location?: string;
  remotePreference?: 'On-site' | 'Remote' | 'Hybrid';
  workAuthorization?: string;
  timezone?: string;
  
  // Research Interests
  primaryInterests: string[];
  methods: string[];
  domains: string[];
  interestStatement?: string;
  
  // Skills
  programmingSkills: Skill[];
  labSkills: string[];
  statisticalSkills: string[];
  
  // Experience
  publications: Publication[];
  projects: Project[];
  workHistory: WorkRole[];
  coursework: string[];
  
  // Availability
  hoursPerWeek: number;
  startDate?: string;
  duration?: 'Semester' | 'Summer' | 'Ongoing';
  compensation?: 'Credit' | 'Stipend' | 'Volunteer';
  creditSeeking: boolean;
  
  // Documents & Links
  cvUrl?: string;
  portfolioUrl?: string;
  googleScholarUrl?: string;
  orcidUrl?: string;
  githubUrl?: string;
  linkedinUrl?: string;
  
  // Privacy
  profileVisibility: 'public' | 'invite-only' | 'private';
  
  // Metadata
  profileCompleteness: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface ProfessorProfile {
  id: string;
  userId: string;
  name: string;
  title: string;
  department: string;
  institution: string;
  researchAreas: string[];
  researchDescription?: string;
  methods: string[];
  publications: Publication[];
  labWebsite?: string;
  googleScholarUrl?: string;
  orcidUrl?: string;
  acceptingStudents: boolean;
  preferredDegreeLevels: ('BS' | 'MS' | 'PhD')[];
  prerequisites?: string;
  contactPreferences: ('in-app' | 'email')[];
  
  // Metadata
  profileCompleteness: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface ResearchProject {
  id: string;
  professorId: string;
  title: string;
  summary: string;
  description: string;
  researchAreas: string[];
  techniques: string[];
  datasets?: string[];
  tools?: string[];
  desiredSkills: Skill[];
  hoursPerWeek: number;
  startWindow: string;
  endWindow?: string;
  compensation: 'Stipend' | 'Credit' | 'Volunteer';
  location: 'On-site' | 'Remote' | 'Hybrid';
  isActive: boolean;
  
  createdAt: Date;
  updatedAt: Date;
}

export interface Skill {
  name: string;
  level: 1 | 2 | 3 | 4 | 5;
}

export interface Publication {
  title: string;
  venue?: string;
  year?: number;
  url?: string;
  doi?: string;
}

export interface Project {
  title: string;
  description: string;
  role: string;
  link?: string;
}

export interface WorkRole {
  title: string;
  organization: string;
  startDate: string;
  endDate?: string;
  description?: string;
}

export interface Match {
  id: string;
  studentId: string;
  professorId?: string;
  projectId?: string;
  matchType: 'professor' | 'project';
  score: number;
  highlights: string[];
  studentInterests: string[];
  professorInterests: string[];
  skillFit: SkillFit[];
  availabilityFit: boolean;
  levelFit: boolean;
  
  createdAt: Date;
}

export interface SkillFit {
  skill: string;
  studentLevel: number;
  requiredLevel: number;
  fit: number;
}

export interface Message {
  id: string;
  threadId: string;
  senderId: string;
  receiverId: string;
  content: string;
  isRead: boolean;
  createdAt: Date;
}

export interface MessageThread {
  id: string;
  participants: string[];
  lastMessage?: Message;
  unreadCount: number;
  createdAt: Date;
  updatedAt: Date;
}

export interface SearchFilters {
  query?: string;
  tags?: string[];
  skills?: string[];
  department?: string;
  level?: string;
  availability?: number;
  remote?: boolean;
  compensation?: string;
  page?: number;
  limit?: number;
}

export interface SearchResult<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  hasMore: boolean;
}

export interface OnboardingStep {
  id: string;
  title: string;
  description: string;
  isCompleted: boolean;
  isRequired: boolean;
}

export interface OnboardingProgress {
  currentStep: number;
  totalSteps: number;
  completedSteps: number;
  progress: number;
}

// API Response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface ApiError {
  code: string;
  message: string;
  fieldErrors?: Record<string, string[]>;
}

// Form schemas (Zod types)
export interface StudentProfileForm {
  basics: {
    firstName: string;
    lastName: string;
    preferredName?: string;
    email: string;
    university: string;
    department: string;
    degreeLevel: 'BS' | 'MS' | 'PhD' | 'Other';
    year: number;
    semester: number;
    gpa?: number;
    graduationTarget?: string;
    location?: string;
    remotePreference?: 'On-site' | 'Remote' | 'Hybrid';
    workAuthorization?: string;
    timezone?: string;
  };
  interests: {
    primaryInterests: string[];
    methods: string[];
    domains: string[];
    interestStatement?: string;
  };
  skills: {
    programmingSkills: Skill[];
    labSkills: string[];
    statisticalSkills: string[];
  };
  experience: {
    publications: Publication[];
    projects: Project[];
    workHistory: WorkRole[];
    coursework: string[];
  };
  availability: {
    hoursPerWeek: number;
    startDate?: string;
    duration?: 'Semester' | 'Summer' | 'Ongoing';
    compensation?: 'Credit' | 'Stipend' | 'Volunteer';
    creditSeeking: boolean;
  };
  links: {
    cvUrl?: string;
    portfolioUrl?: string;
    googleScholarUrl?: string;
    orcidUrl?: string;
    githubUrl?: string;
    linkedinUrl?: string;
  };
  privacy: {
    profileVisibility: 'public' | 'invite-only' | 'private';
  };
}

export interface ProfessorProfileForm {
  basics: {
    name: string;
    title: string;
    department: string;
    institution: string;
  };
  research: {
    researchAreas: string[];
    researchDescription?: string;
    methods: string[];
  };
  publications: Publication[];
  links: {
    labWebsite?: string;
    googleScholarUrl?: string;
    orcidUrl?: string;
  };
  preferences: {
    acceptingStudents: boolean;
    preferredDegreeLevels: ('BS' | 'MS' | 'PhD')[];
    prerequisites?: string;
    contactPreferences: ('in-app' | 'email')[];
  };
}

export interface ProjectForm {
  title: string;
  summary: string;
  description: string;
  researchAreas: string[];
  techniques: string[];
  datasets?: string[];
  tools?: string[];
  desiredSkills: Skill[];
  commitment: {
    hoursPerWeek: number;
    startWindow: string;
    endWindow?: string;
  };
  compensation: 'Stipend' | 'Credit' | 'Volunteer';
  location: 'On-site' | 'Remote' | 'Hybrid';
}

// Taxonomy types
export interface TaxonomyCategory {
  id: string;
  name: string;
  description?: string;
  tags: string[];
}

export interface ResearchArea extends TaxonomyCategory {}
export interface Method extends TaxonomyCategory {}
export interface SkillCategory extends TaxonomyCategory {}

// UI Component props
export interface CardProps {
  className?: string;
  children: React.ReactNode;
}

export interface BadgeProps {
  variant?: 'default' | 'secondary' | 'destructive' | 'outline';
  children: React.ReactNode;
  className?: string;
}

export interface ButtonProps {
  variant?: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link';
  size?: 'default' | 'sm' | 'lg' | 'icon';
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
}
