# MatchEd - Student-Professor Research Matching Platform

A full-stack web application that connects students with professors whose research areas align with their interests, and helps professors discover students that match their active projects.

## 🏗️ Architecture

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and TanStack Query
- **Backend**: Django 5.2 with Django REST Framework and PostgreSQL
- **Communication**: RESTful API with JSON data exchange

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- PostgreSQL
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the backend directory:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=himalayan_db
   DB_USER=postgres
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   GEMINI_API_KEY=your-gemini-api-key
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

7. **Start the backend server**
   ```bash
   python manage.py runserver
   ```

The Django development server will run on `http://localhost:8000/`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables (optional)**
   Create `.env.local` in the frontend directory:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

The Next.js development server will run on `http://localhost:3000/`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Available Endpoints

#### Students
- `GET /api/students/` - List all students
- `GET /api/students/{id}/` - Get specific student
- `POST /api/students/` - Create new student
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student
- `GET /api/students/search/` - Search students with filters

#### Professors
- `GET /api/professors/` - List all professors
- `GET /api/professors/{id}/` - Get specific professor
- `POST /api/professors/` - Create new professor
- `PUT /api/professors/{id}/` - Update professor
- `DELETE /api/professors/{id}/` - Delete professor
- `GET /api/professors/search/` - Search professors with filters

#### Research Projects
- `GET /api/projects/` - List all active projects
- `GET /api/projects/{id}/` - Get specific project
- `POST /api/projects/` - Create new project
- `PUT /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project
- `GET /api/projects/search/` - Search projects with filters

#### Matches
- `GET /api/matches/` - List all matches
- `GET /api/matches/{id}/` - Get specific match
- `POST /api/matches/generate_matches/` - Generate matches for a student

#### Search
- `GET /api/search/global/` - Global search across all entities

## 🧪 Testing the Integration

### 1. Start Both Services
```bash
# Backend (in backend directory)
source venv/bin/activate
python manage.py runserver

# Frontend (in frontend directory)
npm run dev
```

### 2. Access the Test Pages
- Navigate to `http://localhost:3000/api-test` to see the API integration test component
- Navigate to `http://localhost:3000/ai-match-test` to test the AI-enhanced matching functionality

### 3. Test API Endpoints
```bash
# Test students endpoint
curl http://localhost:8000/api/students/

# Test professors endpoint
curl http://localhost:8000/api/professors/

# Test projects endpoint
curl http://localhost:8000/api/projects/
```

## 🏗️ Project Structure

```
himalayan/
├── backend/
│   ├── api/                    # Django API app
│   │   ├── models.py          # Database models
│   │   ├── serializers.py     # API serializers
│   │   ├── views.py           # API views
│   │   └── urls.py            # API URL configuration
│   ├── grad_matcher/          # Django project settings
│   ├── manage.py              # Django management script
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/
│   ├── app/                   # Next.js app directory
│   │   ├── page.tsx           # Home page
│   │   ├── api-test/          # API test page
│   │   └── layout.tsx         # Root layout
│   ├── components/            # React components
│   │   ├── ui/                # UI components
│   │   └── ApiTest.tsx        # API integration test
│   ├── lib/                   # Utility libraries
│   │   ├── api.ts             # API service
│   │   └── hooks.ts           # React Query hooks
│   ├── types/                 # TypeScript type definitions
│   └── package.json           # Node.js dependencies
└── README.md                  # This file
```

## 🔧 Key Features

### Backend Features
- **RESTful API**: Complete CRUD operations for all entities
- **Search & Filtering**: Advanced search across students, professors, and projects
- **AI-Enhanced Matching**: Google Gemini AI-powered intelligent matching algorithm
- **CORS Configuration**: Properly configured for frontend communication
- **Sample Data**: Management command to populate database with test data

### Frontend Features
- **Type-safe API calls** with TypeScript interfaces
- **React Query Integration** for efficient data fetching and caching
- **Modern UI Components** built with Radix UI and Tailwind CSS
- **Error Handling** with custom error boundaries
- **Real-time Updates** with background refetching
- **AI Matching Interface** with toggle between basic and AI-enhanced matching

## 📊 Data Models

### Student Profile
```typescript
interface StudentProfile {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  university: string;
  department: string;
  degreeLevel: 'BS' | 'MS' | 'PhD' | 'Other';
  primaryInterests: string[];
  // ... additional fields
}
```

### Professor Profile
```typescript
interface ProfessorProfile {
  id: string;
  name: string;
  title: string;
  institution: string;
  department: string;
  researchAreas: string[];
  acceptingStudents: boolean;
  // ... additional fields
}
```

### Research Project
```typescript
interface ResearchProject {
  id: string;
  title: string;
  summary: string;
  researchAreas: string[];
  compensation: 'Stipend' | 'Credit' | 'Volunteer';
  location: 'On-site' | 'Remote' | 'Hybrid';
  hoursPerWeek: number;
  // ... additional fields
}
```

## 🛠️ Development

### Adding New API Endpoints
1. Add models in `backend/api/models.py`
2. Create serializers in `backend/api/serializers.py`
3. Add views in `backend/api/views.py`
4. Update URL configuration in `backend/api/urls.py`

### Adding New Frontend Features
1. Create components in `frontend/components/`
2. Add API calls in `frontend/lib/api.ts`
3. Create hooks in `frontend/lib/hooks.ts`
4. Add TypeScript types in `frontend/types/`

## 🔒 Security Considerations

- **CORS**: Properly configured for development
- **Input Validation**: Both frontend and backend validation
- **Type Safety**: TypeScript prevents many runtime errors
- **Error Sanitization**: Errors don't expose sensitive information

## 🚀 Performance Optimizations

1. **Query Caching**: TanStack Query provides intelligent caching
2. **Background Refetching**: Data stays fresh automatically
3. **Optimistic Updates**: UI updates immediately
4. **Pagination**: Large datasets are paginated
5. **Selective Loading**: Only load data when needed

## 🤖 AI Integration

### Google Gemini AI Features
- **Intelligent Profile Analysis**: AI analyzes student and professor profiles to extract key insights
- **Enhanced Matching Algorithm**: Multi-factor scoring including research alignment, skill compatibility, and learning potential
- **Natural Language Explanations**: AI generates human-readable explanations for matches
- **Detailed Score Breakdown**: Individual scores for different matching criteria
- **Fallback System**: Graceful degradation to basic matching when AI is unavailable

### AI Matching Criteria
- **Research Area Alignment** (0-100): How well research interests match
- **Skill Compatibility** (0-100): Technical and methodological skill overlap
- **Academic Level Fit** (0-100): Appropriate educational level matching
- **Availability Match** (0-100): Time commitment and scheduling compatibility
- **Learning Potential** (0-100): Growth and development opportunities

## 🔮 Future Enhancements

1. **Authentication**: JWT-based authentication
2. **Real-time Updates**: WebSocket integration
3. **File Uploads**: Profile pictures and documents
4. **Advanced Search**: Full-text search with Elasticsearch
5. **Notifications**: Real-time notifications for matches
6. **AI Chat Assistant**: Gemini-powered chat for matching guidance
7. **Predictive Analytics**: AI-driven insights on match success probability

## 📝 License

This project is part of a hackathon submission and is not licensed for commercial use.

## 🤝 Contributing

This is a hackathon project. For questions or issues, please contact the development team.
