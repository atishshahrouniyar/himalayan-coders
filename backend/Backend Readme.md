# Himalayan Backend

A Django application with PostgreSQL database for the Himalayan project.

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### Installation

1. **Clone the repository and navigate to backend folder**
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

4. **Set up PostgreSQL database**
   - Create a PostgreSQL database named `himalayan_db`
   - Update the `.env` file with your database credentials

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=himalayan_db
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## Project Structure

```
backend/
├── grad_matcher/          # Django project settings
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables
└── venv/                # Virtual environment
```

## Database

This project uses PostgreSQL as the database. Make sure PostgreSQL is installed and running on your system.

## API Endpoints

The Django development server will run on `http://localhost:8000/`

- Admin interface: `http://localhost:8000/admin/`
- API root: `http://localhost:8000/api/` (when API apps are added)
