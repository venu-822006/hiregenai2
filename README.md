HireGenAI
An AI-powered backend system for intelligent hiring workflows — including resume parsing, authentication, and scalable API services.

Features
User Authentication (JWT + bcrypt)

Resume Parsing (PDF & DOCX support)

Rate Limiting (Flask-Limiter)

Modular Backend Architecture

Async Tasks with Celery

MongoDB Integration

RESTful API Design

Project Structure
Plaintext
hiregenai2/
│
├── app/
│   ├── routes/        # API endpoints
│   ├── models/        # Database models
│   ├── services/      # Business logic
│   ├── utils/         # Helper functions
│   ├── middleware/    # Middleware logic
│   └── errors/        # Error handling
│
├── uploads/           # Uploaded files
├── wsgi.py            # Entry point
├── requirements.txt   # Dependencies
└── .env               # Environment variables
Installation
1. Clone the repository

Bash
git clone https://github.com/your-username/hiregenai.git
cd hiregenai
2. Create virtual environment

Bash
python -m venv .venv
.venv\Scripts\activate   # Windows
3. Install dependencies

Bash
pip install -r requirements.txt

Environment Variables
Create a .env file in the root directory:

Code snippet
MONGO_URI=your_mongodb_connection_string
SECRET_KEY=your_secret_key
REDIS_URL=redis://localhost:6379/0

Run the Application
Bash
python wsgi.py

App will run at: http://127.0.0.1:5000


API Testing
Use tools like:

Postman

Thunder Client

Example endpoints:

POST /register

POST /login

GET  /health

Tech Stack
Backend: Flask

Database: MongoDB

Auth: JWT, bcrypt

Task Queue: Celery + Redis

Parsing: pdfplumber, pdfminer, python-docx

Notes
Ensure MongoDB is running or use MongoDB Atlas.

Redis is required for Celery & rate limiting.

PyMuPDF is excluded due to Python 3.13 compatibility issues.

Deployment
Recommended platforms:

Render

Railway(optional)

Docker (optional)

Contributing
Pull requests are welcome. For major changes, please open an issue first.
