
# Django workshop Project in Docker

Django project that can be run inside a Docker container. Install Docker and Docker Compose.

## Prerequisites

Before you can run this project, ensure that you have the following prerequisites installed on your system:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Getting Started

Follow these steps to run the Django project in a Docker container:

1. **Clone this repository:**

   ```bash
   git clone https://github.com/Aduda-Shem/workshop_phase_2.git
   cd workshop_phase_2
2. **Build the docker image:**
   ```bash
   docker-compose build
3. **Start the Docker container:**
   ```bash
   docker-compose up -d
4. **Apply initial database migrations:**
   ```bash
   docker-compose exec web python manage.py migrate
5. **creating superuser:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
