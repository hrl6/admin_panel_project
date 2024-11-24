# Admin Panel Project

Full-stack admin panel built with Django and Vue.js

## Project Structure
- `backend/` - Django admin panel and REST API
- `frontend/` - Vue.js frontend interface

## Setup Instructions

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend/admin_panel_ui
npm install
npm run dev
```

## Development
- Backend runs on http://localhost:8000
- Frontend runs on http://localhost:5173
- Django admin available at http://localhost:8000/admin
