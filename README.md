# Admin Panel Project

Full-stack admin panel built with Django and Vue.js

## Project Structure
- `backend/` - Django admin panel and REST API
- `frontend/` - Vue.js frontend interface

## Technology Stack
- Backend: Django REST Framework
- Frontend: Vue.js
- Database: PostgreSQL
- Other key technologies used in your project

## Project Structure
* `backend/` - Django admin panel and REST API
* `frontend/` - Vue.js frontend interface

## Prerequisites
Before you begin, ensure you have the following installed:
- Python
- Node.js
- PostgreSQL
- pip
- npm

## Installation & Setup

### Database Setup
1. Create a PostgreSQL database:
```sql
CREATE DATABASE admin_system_db;
```

2. Configure database connection in `backend/settings.py` or through environment variables

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend/admin_panel_ui

# Install dependencies
npm install

# Start development server
npm run dev
```

## Database
- Database migrations should be run with `python manage.py migrate`
- To create new migrations: `python manage.py makemigrations`

## Development
* Frontend runs on http://localhost:5173
* Backend runs on http://localhost:8000/api
* Django admin available at http://localhost:8000/admin

