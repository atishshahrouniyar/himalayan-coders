# MatchEd - Student-Professor Research Matching Platform

A full-stack web application that connects students with professors whose research areas align with their interests, and helps professors discover students that match their active projects.

## 📋 Project Overview

MatchEd is an intelligent research matching platform that uses AI-powered algorithms to create meaningful connections between students and professors in academia. The platform streamlines the process of finding research opportunities and building academic partnerships.

### 🎯 Key Features

- **AI-Powered Matching**: Advanced algorithms using Google's Gemini AI to analyze profiles and create optimal matches
- **Real-time Progress Tracking**: Live updates during the matching process with progress indicators
- **Comprehensive Profiles**: Detailed student and professor profiles with research interests, skills, and preferences
- **Smart Filtering**: Advanced search and filtering capabilities for both students and professors
- **Background Processing**: Non-blocking matching system that processes matches in the background
- **Responsive Design**: Modern, mobile-friendly interface built with Next.js and Tailwind CSS

### 🏗️ Architecture

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS, and Radix UI components
- **Backend**: Django REST Framework with PostgreSQL database
- **AI Integration**: Google Gemini AI for intelligent matching and analysis
- **Real-time Updates**: Polling mechanism for live status updates
- **Session Management**: Client-side session management with localStorage

## 🚀 Setup and Run Instructions

### Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- PostgreSQL database
- Google Gemini API key

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/atishshahrouniyar/himalayan-coders.git
   cd himalayan-coders/backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration:
   # - DATABASE_URL
   # - GEMINI_API_KEY
   # - SECRET_KEY
   ```

5. **Set up database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create sample data (optional)**
   ```bash
   python manage.py create_sample_data
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env.local
   # Edit .env.local with your configuration:
   # - NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Run the development server**
   ```bash
   npm run dev
   ```

### Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/schema/swagger-ui/

## 🛠️ Dependencies and Tools Used

### Frontend Technologies

- **Framework**: Next.js 14 (React-based)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI
- **Icons**: Lucide React
- **State Management**: React Hooks
- **HTTP Client**: Fetch API
- **Build Tool**: Next.js built-in bundler

### Backend Technologies

- **Framework**: Django 4.2+
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **AI Integration**: Google Generative AI (Gemini)
- **API Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Authentication**: Django's built-in auth (extensible)
- **Background Processing**: Python threading
- **Data Validation**: Django model validation

### Development Tools

- **Version Control**: Git
- **Package Manager**: npm (frontend), pip (backend)
- **Code Formatting**: Prettier, Black
- **Linting**: ESLint, Pylint
- **Database**: PostgreSQL
- **API Testing**: Swagger UI, curl
- **Environment Management**: .env files

### External Services

- **AI Service**: Google Gemini API
- **Database**: PostgreSQL (local/cloud)
- **File Storage**: AWS S3 (configured but optional)
- **Email**: SMTP (configured but optional)

## 👥 Team Members and Roles

### Development Team

**Atish Shahrouniyar** - *Full Stack Developer & Project Lead*
- **Role**: Lead developer, architecture design, full-stack implementation
- **Responsibilities**: 
  - Backend API development with Django REST Framework
  - Frontend development with Next.js and TypeScript
  - AI integration with Google Gemini
  - Database design and optimization
  - Real-time matching system implementation
  - Project coordination and deployment

### Key Contributions

- **AI-Powered Matching Algorithm**: Implemented intelligent matching using Gemini AI
- **Real-time Progress Tracking**: Built background processing with live status updates
- **Responsive UI/UX**: Created modern, mobile-friendly interface
- **API Design**: RESTful API with comprehensive documentation
- **Database Architecture**: Optimized schema for matching and user management
- **Session Management**: Client-side session handling without authentication overhead

### Development Process

- **Agile Methodology**: Iterative development with continuous feedback
- **Version Control**: Git-based workflow with feature branches
- **Testing**: Manual testing with automated test scripts
- **Documentation**: Comprehensive API documentation with Swagger
- **Deployment**: Ready for production deployment

## 📁 Project Structure

```
himalayan/
├── backend/                 # Django backend
│   ├── api/                # Main application
│   │   ├── models.py       # Database models
│   │   ├── views.py        # API endpoints
│   │   ├── serializers.py  # Data serialization
│   │   ├── matching_service.py  # Matching logic
│   │   └── gemini_service.py    # AI integration
│   ├── grad_matcher/       # Django settings
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── app/               # App router pages
│   ├── components/        # Reusable components
│   ├── lib/              # Utility functions
│   └── package.json      # Node dependencies
└── README.md             # This file
```

## 🔧 API Endpoints

### Core Endpoints

- `GET /api/students/` - List all students
- `POST /api/students/` - Create new student profile
- `GET /api/professors/` - List all professors
- `POST /api/professors/` - Create new professor profile
- `GET /api/matches/` - Get matches with filtering
- `GET /api/students/{id}/matching_status/` - Get matching progress

### Authentication

Currently using session-based management with localStorage. Ready for JWT or OAuth integration.

## 🚀 Deployment

### Production Setup

1. **Environment Variables**: Configure production environment variables
2. **Database**: Set up PostgreSQL production database
3. **Static Files**: Configure static file serving
4. **SSL**: Set up HTTPS certificates
5. **Monitoring**: Add logging and monitoring

### Deployment Options

- **Vercel**: Frontend deployment
- **Railway/Heroku**: Backend deployment
- **AWS**: Full-stack deployment
- **Docker**: Containerized deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Contact

- **Email**: contact@matched.com
- **GitHub**: [atishshahrouniyar/himalayan-coders](https://github.com/atishshahrouniyar/himalayan-coders)

---

**MatchEd** - Connecting students and professors for meaningful research partnerships.
