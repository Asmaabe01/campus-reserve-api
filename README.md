# CampusReserve API

<p align="center">
  <b>A modern backend API for booking campus rooms, labs, equipment, and shared resources.</b>
</p>

<p align="center">
  Built with FastAPI and designed to grow into a secure, testable, production-style booking platform.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Uvicorn-ASGI-499848" alt="Uvicorn" />
  <img src="https://img.shields.io/badge/Status-In%20Development-orange" alt="Status" />
</p>

---

## Overview

**CampusReserve API** is a backend system for managing reservations of shared campus resources such as:

- Study rooms
- Laboratories
- Projectors
- Sports facilities
- Equipment
- Other reservable campus spaces

The goal of the project is to build a realistic booking system with authentication, permissions, availability checks, overlap prevention, testing, database migrations, and containerized deployment.

---

## Current Status

The project is currently in the **foundation stage**.

### Implemented

- FastAPI application setup
- Root API endpoint
- Swagger documentation
- ReDoc documentation
- Virtual environment setup
- Dependency management
- Git and GitHub repository setup

---

## Planned Features

### Authentication

- User registration
- User login
- Password hashing
- JWT authentication
- Protected routes

### Resource Management

- Create campus resources
- View available resources
- Resource categories
- Capacity
- Location
- Availability status

### Booking System

- Create reservations
- Start and end times
- Cancel reservations
- View personal booking history
- Prevent overlapping bookings
- Validate booking time ranges
- Prevent double booking

### Permissions

- Standard users
- Admin users
- Restricted resource management
- Booking approval where required

### Backend Infrastructure

- PostgreSQL
- SQLModel
- Alembic migrations
- Pytest
- Docker
- Docker Compose
- Environment-based configuration

---

## Core Booking Logic

One of the main goals of this project is to prevent booking conflicts.

Example:

```text
User A books Room 101
10:00 → 11:00

User B tries to book Room 101
10:30 → 11:30

Result:
Booking rejected because the time ranges overlap.
```

The API will check existing reservations before creating a new booking.

---

## Planned Architecture

```text
Client
  │
  ▼
FastAPI
  │
  ├── Authentication
  │
  ├── Resource Management
  │
  └── Booking Logic
  │
  ▼
SQLModel
  │
  ▼
PostgreSQL
```

---

## Project Structure

```text
campus-reserve-api/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

The structure will expand as new modules are added.

---

## API Endpoints

### Current Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Returns the API welcome message |

More endpoints will be added as development continues.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Asmaabe01/campus-reserve-api.git
cd campus-reserve-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the development server

```bash
python -m uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates interactive documentation.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## Development Roadmap

```text
Phase 1
FastAPI foundation
        ↓
Phase 2
Database + models
        ↓
Phase 3
Authentication
        ↓
Phase 4
Resource management
        ↓
Phase 5
Booking logic
        ↓
Phase 6
Permissions + validation
        ↓
Phase 7
Testing + Docker
        ↓
Phase 8
Deployment
```

---

## Learning Goals

This project is being built to strengthen practical backend development skills, including:

- REST API design
- FastAPI architecture
- Database modeling
- Relational data design
- Authentication and authorization
- Business logic
- Booking conflict detection
- API validation
- Testing
- Database migrations
- Docker
- Git workflow
- Production-oriented project structure

---

## Future Tech Stack

As the project grows, it is planned to use:

| Technology | Purpose |
|---|---|
| FastAPI | API framework |
| SQLModel | ORM and data models |
| PostgreSQL | Database |
| Alembic | Database migrations |
| JWT | Authentication |
| Pwdlib | Password hashing |
| Pytest | Automated testing |
| Docker | Containerization |
| Docker Compose | Multi-container setup |
| GitHub Actions | CI/CD |

---

## Project Status

> 🚧 **In active development**

The repository is being built incrementally, with each stage focused on learning and implementing real backend engineering concepts.

---

## Author

**Asmae Bequi**

- [GitHub](https://github.com/Asmaabe01)
- [LinkedIn](https://www.linkedin.com/in/asmaa-bequi-609070422/)
- [LeetCode](https://leetcode.com/u/asmaebequi/)
