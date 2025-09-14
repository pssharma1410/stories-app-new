🎬 Django Stories API

A robust, containerized backend API for a story-sharing platform built with Django and Celery, featuring asynchronous task processing, scalable architecture, and Docker-based deployment.

🚀 Table of Contents

🌐 Technology Stack

📂 Project Structure

🛠 Prerequisites

⚡ Setup & Installation

🏃 Running the Application

🧰 Available Commands

🛑 Stopping the Application

🌐 Technology Stack
Layer	Technology
Backend	Python 3.11, Django 5.2, Django REST Framework
Database	PostgreSQL 15
Asynchronous Tasks	Celery 5
Message Broker & Cache	Redis 7
Containerization	Docker & Docker Compose
WSGI Server	Gunicorn
📂 Project Structure
.
├── api/                  # Main Django project directory
│   ├── manage.py         # Django CLI for tasks
│   └── ...               # Django apps and project files
├── .env                  # Local environment variables
├── .env.example          # Template for env variables
├── docker-compose.yml    # Multi-container setup
├── Dockerfile            # Docker image build instructions
├── Makefile              # Developer-friendly shortcuts
├── requirements.txt      # Python dependencies
└── start.sh              # Entrypoint script for the web container


Tip: You can explore each Django app under api/ for models, views, serializers, and API endpoints.

🛠 Prerequisites

Before starting, ensure you have the following installed:

Docker – Installation Guide

Docker Compose – Installation Guide

Note: No local Python or database installation is required — everything runs in containers!

⚡ Setup & Installation
1️⃣ Clone the repository
git clone <your-repo-url>
cd <your-project-folder>

2️⃣ Configure Environment Variables

Copy the example environment file:

cp .env.example .env


This file contains database credentials, Django secret key, and other settings needed for the app.

🏃 Running the Application
1️⃣ Start All Services

Using Makefile:

make dev


Or using docker-compose directly:

docker-compose up --build


Once running, the API will be available at: http://localhost:8000

2️⃣ Initial Database Migrations (Automatic)

The start.sh script automatically applies migrations. ✅ No manual action needed.

3️⃣ Create a Superuser

To access Django admin:

make superuser


Follow the prompts, then login at: http://localhost:8000/admin/

🧰 Available Commands
Command	Description
make dev	Build & start all Docker containers
make migrate	Run Django database migrations manually
make superuser	Create a Django admin superuser
make worker	Start a Celery worker (debug mode)
make lint	Check Python code style with flake8
make test	Run tests using pytest

Tip: You can also run docker-compose exec web bash to enter the container shell for debugging.

🛑 Stopping the Application

Stop and remove all containers, networks, and volumes:

docker-compose down


Stop containers without removing them:

Ctrl+C
# or
docker-compose stop
