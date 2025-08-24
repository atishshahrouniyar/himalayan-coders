# Swagger/OpenAPI Documentation for MatchEd API

This document describes the Swagger/OpenAPI integration for the MatchEd Django backend.

## Overview

The API documentation is generated using `drf-spectacular`, which automatically creates OpenAPI 3.0 compliant documentation from your Django REST Framework views and serializers.

## Available Documentation Endpoints

Once the Django server is running, you can access the API documentation at:

### 1. OpenAPI Schema (JSON)
- **URL**: `http://localhost:8000/api/schema/`
- **Description**: Raw OpenAPI 3.0 JSON schema
- **Use Case**: For programmatic access or integration with other tools

### 2. Swagger UI
- **URL**: `http://localhost:8000/api/docs/`
- **Description**: Interactive Swagger UI for testing API endpoints
- **Features**:
  - Interactive API documentation
  - Try-it-out functionality
  - Request/response examples
  - Authentication support

### 3. ReDoc
- **URL**: `http://localhost:8000/api/redoc/`
- **Description**: Alternative documentation interface with a different layout
- **Features**:
  - Clean, responsive design
  - Better for reading documentation
  - Mobile-friendly

## API Endpoints Documentation

The API is organized into the following categories:

### Students (`/api/students/`)
- **List students**: `GET /api/students/`
- **Create student**: `POST /api/students/`
- **Get student details**: `GET /api/students/{id}/`
- **Update student**: `PUT /api/students/{id}/`
- **Delete student**: `DELETE /api/students/{id}/`
- **Search students**: `GET /api/students/search/`

### Professors (`/api/professors/`)
- **List professors**: `GET /api/professors/`
- **Create professor**: `POST /api/professors/`
- **Get professor details**: `GET /api/professors/{id}/`
- **Update professor**: `PUT /api/professors/{id}/`
- **Delete professor**: `DELETE /api/professors/{id}/`
- **Search professors**: `GET /api/professors/search/`

### Research Projects (`/api/projects/`)
- **List projects**: `GET /api/projects/`
- **Create project**: `POST /api/projects/`
- **Get project details**: `GET /api/projects/{id}/`
- **Update project**: `PUT /api/projects/{id}/`
- **Delete project**: `DELETE /api/projects/{id}/`
- **Search projects**: `GET /api/projects/search/`

### Matches (`/api/matches/`)
- **List matches**: `GET /api/matches/`
- **Create match**: `POST /api/matches/`
- **Get match details**: `GET /api/matches/{id}/`
- **Update match**: `PUT /api/matches/{id}/`
- **Delete match**: `DELETE /api/matches/{id}/`
- **Generate AI matches**: `POST /api/matches/generate_matches/`

### Global Search (`/api/search/`)
- **Global search**: `GET /api/search/global_search/`

## Configuration

The Swagger configuration is defined in `grad_matcher/settings.py`:

```python
# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# Spectacular Configuration
SPECTACULAR_SETTINGS = {
            'TITLE': 'MatchEd API',
    'DESCRIPTION': 'Student-Professor Research Matching Platform API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
    'CONTACT': {
        'name': 'MatchEd Team',
        'email': 'support@matched.com',
    },
    'LICENSE': {
        'name': 'MIT License',
        'url': 'https://opensource.org/licenses/MIT',
    },
    'TAGS': [
        {'name': 'students', 'description': 'Student profile management'},
        {'name': 'professors', 'description': 'Professor profile management'},
        {'name': 'projects', 'description': 'Research project management'},
        {'name': 'matches', 'description': 'AI-powered matching system'},
    ],
}
```

## URL Configuration

The Swagger URLs are configured in `grad_matcher/urls.py`:

```python
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    
    # Swagger/OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
```

## Features

### Automatic Documentation Generation
- All ViewSets and their actions are automatically documented
- Serializer schemas are automatically included
- Request/response examples are generated from your code

### Enhanced Documentation
- Custom descriptions and summaries for each endpoint
- Parameter descriptions and examples
- Request body schemas with examples
- Response schemas with examples

### Search and Filtering
- All search endpoints include detailed parameter documentation
- Query parameter descriptions and examples
- Support for multiple parameter types

### AI Matching Documentation
- Detailed documentation for the AI-enhanced matching system
- Request body schemas for match generation
- Examples for different match types (professor vs project)

## Usage Examples

### Using Swagger UI
1. Navigate to `http://localhost:8000/api/docs/`
2. Browse the available endpoints by category
3. Click on any endpoint to see its documentation
4. Use the "Try it out" button to test the endpoint
5. View the request/response schemas and examples

### Using ReDoc
1. Navigate to `http://localhost:8000/api/redoc/`
2. Browse the documentation in a clean, readable format
3. Use the search functionality to find specific endpoints
4. View detailed schemas and examples

### Programmatic Access
```bash
# Get the OpenAPI schema
curl http://localhost:8000/api/schema/ > api_schema.json

# Use with other tools
# - Import into Postman
# - Generate client libraries
# - Use with API testing tools
```

## Dependencies

The Swagger integration requires the following packages:
- `drf-spectacular==0.27.0`
- `Django>=2.2`
- `djangorestframework>=3.10.3`

## Troubleshooting

### Common Issues

1. **Schema not generating**: Make sure `drf_spectacular` is in `INSTALLED_APPS`
2. **URLs not working**: Check that the Swagger URLs are properly configured in `urls.py`
3. **Missing documentation**: Ensure your views have proper docstrings and use `@extend_schema` decorators

### Debugging

1. Check Django logs for any errors
2. Verify that the server is running on the correct port
3. Test the schema endpoint directly: `curl http://localhost:8000/api/schema/`

## Future Enhancements

- Add authentication documentation
- Include more detailed response examples
- Add webhook documentation
- Implement API versioning
- Add rate limiting documentation
