I’ve made it descriptive, covering setup, usage, and features:

# SSL Monitoring Application

A web-based application to monitor SSL certificates, sync them from an Identity Management (IDM/IPA) server, and provide insights on certificate expiry.

---

## Features

- View all SSL certificates in a dashboard
- Add or delete certificates manually
- Sync certificates automatically from IDM/IPA server
- Calculate days left until certificate expiry
- PostgreSQL database backend
- Containerized using Docker and Docker Compose

---

## Technologies Used

- **Backend:** Python, Flask, SQLAlchemy
- **Database:** PostgreSQL
- **Containerization:** Docker, Docker Compose
- **Frontend:** HTML, CSS, Jinja2 templates

---

## Prerequisites

- Docker & Docker Compose installed
- Access to IDM/IPA server (optional for sync)
- GitHub account for source code (optional)
- Python 3.10+ for local testing (optional)

---

## Installation & Setup

1. **Clone the repository:**

```bash
git clone https://github.com/ramineniramesh505/SSLMonitoringApplication.git
cd SSLMonitoringApplication


Build and start the Docker containers:

docker-compose up --build -d


Access the application:

Web UI: http://localhost:444

PostgreSQL: localhost:5432 (credentials in .env or docker-compose.yml)

Project Structure
ssl-manager/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── app.py
├── models.py
├── sync_from_ipa.py
├── db/
│   └── init.sql
├── templates/
│   └── index.html
└── static/

Environment Variables

DATABASE_URL – PostgreSQL connection string

IPA_URL – IDM/IPA server URL for syncing certificates

IPA_USER – IDM username

IPA_PASS – IDM password

Usage

Start the application using Docker Compose.

Open the web UI at http://localhost:444.

Add new SSL certificates manually via the form.

Sync certificates from IDM automatically using the ssl-sync service.

Notes

Ensure your network allows connection to the IDM/IPA server if using automatic sync.

SSL certificates are stored in PostgreSQL for persistence.

The application is fully containerized for easy deployment.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Author

Ramineni Ramesh – GitHub
